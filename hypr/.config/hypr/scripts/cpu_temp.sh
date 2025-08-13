#!/bin/bash

# Nome do processador (extraído dinamicamente)
CPU_NAME=$(grep -m 1 'model name' /proc/cpuinfo | sed 's/.*: //')

# Obtém a temperatura da CPU
CPU_TEMP=$(sensors | grep -oP 'Tctl:\s+\+\K[0-9.]+' | awk '{printf "%d", $1}')
# Caso a primeira linha não retorne temperatura, tenta uma segunda alternativa
if [[ -z "$CPU_TEMP" ]]; then
    CPU_TEMP=$(sensors | grep -oP 'Package id 0:\s+\+\K[0-9.]+' | awk '{printf "%d", $1}')
fi

# Tooltip com o nome do processador
TOOLTIP="$CPU_NAME"

# Verifica se a temperatura foi obtida e monta o JSON
if [[ -n "$CPU_TEMP" ]]; then
    echo "{\"text\": \"${CPU_TEMP}°C\", \"tooltip\": \"$TOOLTIP\"}"
else
    echo "{\"text\": \"N/A\", \"tooltip\": \"$TOOLTIP\"}"
fi
