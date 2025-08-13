# dotfiles do Vinicius (Hyprland / Waybar / GTK / Qt / Kitty / Rofi)

Configurações completas do meu ambiente Arch Linux com Hyprland, Waybar, GTK, Qt, Kitty, Rofi e mais. Inclui script de instalação automatizado com bootstrap de pacotes, AUR e Stow.

## Pré‑requisitos
- Arch Linux (ou derivado com `pacman`)
- Acesso sudo
- Conexão à internet

## O que está incluído
- Hyprland: configs em `hypr/.config/hypr`
- Waybar: temas, módulos e scripts em `waybar/.config/waybar`
- Kitty: configs em `kitty/.config/kitty`
- Rofi: tema e layout em `rofi/.config/rofi`
- btop: `btop/.config/btop`
- GTK 3/4: `gtk3/.config/gtk-3.0`, `gtk4/.config/gtk-4.0`
- xsettingsd: `xsettingsd/.config/xsettingsd`
- Qt5ct: `qt5ct/.config/qt5ct`
- Code - OSS: `code-oss/.config/Code - OSS/User`
- Extras em `config/.config` (assets, nwg-look, ksnip, user-dirs, mimeapps)
- Shell: `.bashrc` em `shell/.bashrc`
- Ícones locais: `icons/.local/share/icons`
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
- Instalar `stow` (e `yay` se necessário) via `pacman`
- Instalar pacotes do `bootstrap/pacman.txt` e AUR do `bootstrap/aur.txt`
- Stow de todos os pacotes para `$HOME`
- Instalar extensões do Code‑OSS se presentes
- Tentar recarregar Hyprland/Waybar se estiverem rodando

## Personalização
- Adicione novos pacotes aos arquivos em `bootstrap/`
- Coloque novos diretórios de configuração seguindo o padrão: `<pkg>/.config/<nome>` e eles serão stowados
- Para fontes/ícones de usuário, use `icons/.local/share/icons` (e `fonts` se criar)

## Dicas
- Atualizar dotfiles com alterações locais:
  ```bash
  # Exemplo: sincronizar alterações locais para o repositório
  rsync -avh --delete ~/.config/hypr/ hypr/.config/hypr/
  rsync -avh --delete ~/.config/waybar/ waybar/.config/waybar/
  ```
- Fazer commit e push:
  ```bash
  git add -A
  git commit -m "Atualiza configs"
  git push
  ```

## Licença
MIT
