#!/bin/bash
#  _____                           _             _            
# |_   _|__ _ __ _ __ ___  _ __  | |_ _ __ ___ (_)_ __   ___ 
#   | |/ _ \ '__| '_ ` _ \| '_ \ | __| '_ ` _ \| | '_ \ / _ \
#   | |  __/ |  | | | | | | |_) || |_| | | | | | | | | |  __/
#   |_|\___|_|  |_| |_| |_| .__/  \__|_| |_| |_|_|_| |_|\___|
#                          |_|                                

# Arquivo de cache para controlar o estado
cache_file="$HOME/.cache/transparency_toggle"

# Função para ativar transparência
enable_transparency() {
    hyprctl keyword decoration:active_opacity 0.95
    hyprctl keyword decoration:inactive_opacity 0.85
    hyprctl keyword decoration:blur:enabled true
    echo "enabled" > "$cache_file"
    notify-send "Transparência Ativada" "Janelas agora são semi transparentes"
}

# Função para desativar transparência
disable_transparency() {
    hyprctl keyword decoration:active_opacity 1.0
    hyprctl keyword decoration:inactive_opacity 1.0
    hyprctl keyword decoration:blur:enabled false
    echo "disabled" > "$cache_file"
    notify-send "Transparência Desativada" "Janelas agora são totalmente opacas"
}

# Verificar estado atual e alternar
if [ -f "$cache_file" ] && [ "$(cat "$cache_file")" = "enabled" ]; then
    disable_transparency
else
    enable_transparency
fi 