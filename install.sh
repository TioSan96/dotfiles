#!/usr/bin/env bash
set -Eeuo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$REPO_DIR"

if ! command -v stow >/dev/null 2>&1; then
  echo "Installing stow..." >&2
  if command -v pacman >/dev/null 2>&1; then
    sudo pacman -S --needed --noconfirm stow
  else
    echo "pacman not found; install GNU Stow manually." >&2
    exit 1
  fi
fi

if command -v yay >/dev/null 2>&1; then
  AUR_HELPER="yay"
elif command -v paru >/dev/null 2>&1; then
  AUR_HELPER="paru"
else
  AUR_HELPER=""
fi

# Packages
if [ -f bootstrap/pacman.txt ]; then
  echo "Installing pacman packages..."
  sudo pacman -S --needed --noconfirm $(grep -vE '^(linux|linux-zen|linux-zen-headers)$' bootstrap/pacman.txt | tr '\n' ' ')
fi
# AUR helper bootstrap (if needed)
if [ -f bootstrap/aur.txt ] && [ -s bootstrap/aur.txt ]; then
  if [ -z "${AUR_HELPER}" ]; then
    echo "No AUR helper found. Bootstrapping yay..."
    sudo pacman -S --needed --noconfirm git base-devel
    tmpdir="$(mktemp -d)"
    trap 'rm -rf "$tmpdir"' EXIT
    (
      cd "$tmpdir"
      git clone https://aur.archlinux.org/yay-bin.git
      cd yay-bin
      makepkg -si --noconfirm
    )
    if command -v yay >/dev/null 2>&1; then
      AUR_HELPER="yay"
    fi
  fi
  if [ -n "${AUR_HELPER}" ]; then
    echo "Installing AUR packages with ${AUR_HELPER}..."
    ${AUR_HELPER} -S --needed --noconfirm $(cat bootstrap/aur.txt | tr '\n' ' ')
  else
    echo "AUR helper not available. Skipping AUR packages." >&2
  fi
fi

# Dotfiles with Stow
# Add new packages here to be stowed into $HOME
for pkg in hypr waybar kitty rofi btop gtk3 gtk4 xsettingsd qt5ct code-oss config shell icons wallpapers; do
  if [ -d "$pkg" ]; then
    echo "Stowing $pkg"
    stow -v -R -t "$HOME" "$pkg"
  fi
done

# VS Code OSS extensions
if command -v code >/dev/null 2>&1 && [ -f bootstrap/code-extensions.txt ]; then
  echo "Installing VS Code OSS extensions..."
  while IFS= read -r ext; do
    [ -n "$ext" ] || continue
    code --install-extension "$ext" --force || true
  done < bootstrap/code-extensions.txt
fi

# Post steps: reload Hyprland/Waybar if running
if pgrep -x hyprland >/dev/null 2>&1; then
  hyprctl reload || true
fi
if pgrep -x waybar >/dev/null 2>&1; then
  pkill -SIGUSR2 waybar || pkill -HUP waybar || true
fi

echo "All done."
