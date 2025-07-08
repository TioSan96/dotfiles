#!/bin/bash

# Detecta o nome da GPU automaticamente usando lspci
GPU_NAME=$(lspci | grep -i "vga" | awk -F': ' '{print $2}')

# Obtém a temperatura da GPU
GPU_TEMP=$(sensors | grep -oP 'edge:\s+\+\K[0-9.]+' | awk '{printf "%d", $1}')

# Tooltip com o nome da GPU
TOOLTIP="$GPU_NAME"

# Verifica se a temperatura foi obtida e monta o JSON
if [[ -n "$GPU_TEMP" ]]; then
    echo "{\"text\": \"${GPU_TEMP}°C\", \"tooltip\": \"$TOOLTIP\"}"
else
    echo "{\"text\": \"N/A\", \"tooltip\": \"$TOOLTIP\"}"
fi
