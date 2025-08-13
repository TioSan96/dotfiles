#!/bin/bash
LOG_FILE="$HOME/.config/hypr/update_icons.log"

echo "Executando script update_icons.sh em $(date)" > "$LOG_FILE"

ICONS_DIR="$HOME/.icons"

if [ -d "$ICONS_DIR" ]; then
    for dir in "$ICONS_DIR"/*; do
        if [ -d "$dir" ]; then
            gtk-update-icon-cache "$dir" && echo "Cache atualizado para $dir" >> "$LOG_FILE"
        fi
    done
else
    echo "Pasta ~/.icons não encontrada." >> "$LOG_FILE"
fi

echo "Finalizado em $(date)" >> "$LOG_FILE"
