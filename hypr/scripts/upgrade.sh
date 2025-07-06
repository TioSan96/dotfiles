#!/bin/bash

# Envia uma notificação inicial para o dunst
notify-send "Atualização do Sistema" "Iniciando a atualização do sistema..."

# Inicia a atualização do sistema
echo "Iniciando a atualização do sistema..."

# Atualiza pacotes do Arch com yay
yay -Syu --noconfirm

# Atualiza pacotes do Arch com pacman
sudo pacman -Syu --noconfirm

# Atualiza Flatpak
#flatpak update -y

# Envia uma notificação do dunst informando que a atualização foi concluída
notify-send "Atualização do Sistema" "Sistema atualizado com sucesso!"

# Envia o sinal para recarregar a Waybar e zerar o contador
pkill -SIGRTMIN+8 waybar

# Recarregando as config da Waybar
hyprctl reload 

# Exibe mensagem de sucesso
echo "Sistema atualizado com sucesso!"

# Aguarda o pressionamento da tecla Enter para fechar o terminal
#echo "Pressione Enter para fechar..."
#read -r
sleep 10
# Força o encerramento do terminal se estiver no Kitty
if [ "$KITTY_WINDOW_ID" ]; then
    kitty @ close-window
else
    exit
fi


