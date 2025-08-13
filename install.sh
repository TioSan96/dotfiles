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

# Dolphin viewers and codecs
echo "Installing Dolphin viewers (Gwenview/MPV/Okular) and extras..."
sudo pacman -S --needed --noconfirm gwenview mpv okular kio-extras kimageformats libheif || true

# MIME defaults
echo "Applying user MIME defaults..."
xdg-mime default org.kde.dolphin.desktop inode/directory || true
xdg-mime default org.kde.gwenview.desktop image/jpeg image/png image/webp image/gif image/bmp image/tiff image/svg+xml image/avif image/heif || true
xdg-mime default mpv.desktop video/mp4 video/x-matroska video/webm video/x-msvideo video/x-ms-wmv video/quicktime || true
xdg-mime default org.kde.okular.desktop application/pdf application/epub+zip application/x-djvu || true
xdg-mime default org.kde.ark.desktop application/zip application/x-7z-compressed application/x-rar application/x-xz application/gzip application/x-bzip2 application/x-tar || true
xdg-mime default code-oss.desktop text/plain text/x-shellscript application/json application/x-yaml text/markdown || true

# GTK/Qt theming defaults
echo "Configuring GTK/Qt themes..."
gsettings set org.gnome.desktop.interface color-scheme "prefer-dark" || true
gsettings set org.gnome.desktop.interface gtk-theme "Breeze-Dark" || true
gsettings set org.gnome.desktop.interface icon-theme "Papirus-Dark" || true
gsettings set org.gnome.desktop.interface cursor-theme "Bibata-Modern-Ice" || true
gsettings set org.gnome.desktop.interface font-name "JetBrainsMonoNL Nerd Font Mono 11" || true

# Qt (qt5ct/qt6ct) config skeletons if not present
mkdir -p "$HOME/.config/qt5ct" "$HOME/.config/qt6ct"
printf "[Appearance]\nicon_theme=Papirus-Dark\nstyle=Breeze\n" > "$HOME/.config/qt5ct/qt5ct.conf" || true
printf "[Appearance]\nicon_theme=Papirus-Dark\nstyle=Breeze\n" > "$HOME/.config/qt6ct/qt6ct.conf" || true

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

# Git personalization for Vinicius
echo "Configuring Git and SSH for Vinicius..."
git config --global user.name "Vinicius" || true
git config --global user.email "skskskm@hotmail.com" || true
git config --global init.defaultBranch main || true

# SSH key setup (ed25519) if not exists
if [ ! -f "$HOME/.ssh/id_ed25519" ]; then
  mkdir -p "$HOME/.ssh"
  ssh-keygen -t ed25519 -C "skskskm@hotmail.com" -N "" -f "$HOME/.ssh/id_ed25519" || true
fi
eval "$(ssh-agent -s)" >/dev/null 2>&1 || true
ssh-add "$HOME/.ssh/id_ed25519" >/dev/null 2>&1 || true

# If repo remote is HTTPS, switch to SSH
if git -C "$REPO_DIR" remote get-url origin 2>/dev/null | grep -q '^https://github.com/'; then
  git -C "$REPO_DIR" remote set-url origin "git@github.com:TioSan96/dotfiles.git" || true
fi

echo "Add this SSH key to GitHub → Settings → SSH keys:"
if [ -f "$HOME/.ssh/id_ed25519.pub" ]; then
  cat "$HOME/.ssh/id_ed25519.pub"
fi
