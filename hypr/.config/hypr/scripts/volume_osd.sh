#!/bin/bash

# Obter o volume atual
VOLUME=$(pamixer --get-volume) # Alternativamente: pactl get-sink-volume @DEFAULT_SINK@ | grep -oP '\d+%' | head -1

# Verificar se está mutado
if pamixer --get-mute; then
  ICON="audio-volume-muted"
  MESSAGE="Áudio Mutado"
else
  # Selecionar ícone com base no nível de volume
  if [ "$VOLUME" -eq 0 ]; then
    ICON="audio-volume-muted"
  elif [ "$VOLUME" -le 30 ]; then
    ICON="audio-volume-low"
  elif [ "$VOLUME" -le 70 ]; then
    ICON="audio-volume-medium"
  else
    ICON="audio-volume-high"
  fi
  MESSAGE="Volume: ${VOLUME}%"
fi

# Enviar notificação
notify-send -a "Volume" -u low -i "$ICON" "$MESSAGE"
