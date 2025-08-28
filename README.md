# dotfiles de TioSan96

Configurações completas do meu ambiente Arch Linux com Hyprland, Waybar, GTK, Qt, Warp, Rofi e mais. Inclui script de instalação automatizado com bootstrap de pacotes, AUR e Stow.

## Pré‑requisitos
- Arch Linux (ou derivado com `pacman`)
- Acesso sudo
- Conexão à internet

## Preview
![Preview](assets/preview.png)

## Novidades em v2.0
- Notificador: migração para `mako` (substitui `dunst`) com visual unificado ao Hyprland (borda e fundo `#4169E1`, raio `5`, ícones ativados).
- Terminal padrão: `warp-terminal` (substitui `kitty` como padrão; configs do `kitty` permanecem disponíveis no repo).
- Installer: passou a stowar o pacote `mako` e incluir `libnotify` (notify-send) no bootstrap pacman. Adicionado `warp-terminal` no AUR.
- Hyprland: `exec-once = mako` adicionado ao autostart e `$terminal = warp-terminal`.

## O que está incluído
- Hyprland: configs em `hypr/.config/hypr`
- Waybar: temas, módulos e scripts em `waybar/.config/waybar`
- Mako: configuração em `mako/.config/mako`
- Kitty (opcional): configs em `kitty/.config/kitty`
- Rofi: tema e layout em `rofi/.config/rofi`
- btop: `btop/.config/btop`
- GTK 3/4: `gtk3/.config/gtk-3.0`, `gtk4/.config/gtk-4.0`
- xsettingsd: `xsettingsd/.config/xsettingsd`
- Qt5ct/Qt6ct: `qt5ct/.config/qt5ct`, `qt6ct` (gerado no install)
- Code - OSS: `code-oss/.config/Code - OSS/User`
- Extras em `config/.config` (assets, nwg-look, ksnip, user-dirs, mimeapps)
- Shell: `.bashrc` em `shell/.bashrc`
- Ícones locais: `icons/.local/share/icons`
- Wallpapers: `wallpapers/.local/share/backgrounds/kisamew.jpg` (usado pelo Hyprland via `swww`)
- Bootstrap de pacotes: `bootstrap/pacman.txt`, `bootstrap/aur.txt`
- Extensões do Code OSS: `bootstrap/code-extensions.txt`

## Instalação (após formatar)
```bash
git clone git@github.com:TioSan96/dotfiles.git ~/dotfiles
cd ~/dotfiles
chmod +x install.sh
./install.sh
```

O script irá:
- Instalar `stow` (e `yay` se necessário)
- Instalar pacotes do `bootstrap/pacman.txt` e AUR do `bootstrap/aur.txt`
- Stow de todos os pacotes para `$HOME`
- Configurar temas:
  - GTK: Breeze‑Dark, ícones Papirus‑Dark, cursor Bibata‑Modern‑Ice, fonte JetBrainsMonoNL Nerd Font Mono 11
  - Qt: `qt5ct`/`qt6ct` com tema Breeze e ícones Papirus‑Dark
- Tentar recarregar Hyprland/Waybar se estiverem rodando

## Personalização
- Ajuste temas no `qt5ct`/`qt6ct` e `gsettings` conforme preferir
- Adicione novos pacotes aos arquivos em `bootstrap/`
- Coloque novos diretórios de configuração seguindo o padrão: `<pkg>/.config/<nome>` e eles serão stowados

## Dicas
- Atualizar dotfiles com alterações locais:
  ```bash
  rsync -avh --delete ~/.config/hypr/ hypr/.config/hypr/
  rsync -avh --delete ~/.config/waybar/ waybar/.config/waybar/
  rsync -avh --delete ~/.config/mako/ mako/.config/mako/
  ```
- Fazer commit e push:
  ```bash
  git add -A
  git commit -m "Atualiza configs"
  git push
  ```

## Changelog

### v2.0
- `mako` como daemon de notificações (visual unificado ao Hyprland)
- `warp-terminal` como terminal padrão
- Installer atualizado (stow de `mako`, `libnotify` em pacman e `warp-terminal` no AUR)
- Hyprland atualizado com autostart de `mako`

### v1.x
- Configurações originais com `kitty`, Waybar, Hyprland e demais pacotes

## Licença
MIT
