#!/bin/bash

# Verifica se há algum áudio sendo reproduzido
audio_playing=$(pactl list short sink-inputs | wc -l)

# Verifica se há algum processo de vídeo em execução
video_playing=$(ps aux | grep -E 'ffmpeg|vlc|mpv|youtube-dl|stremio' | grep -v 'grep' | wc -l)

# Verifica se há mídia sendo reproduzida com playerctl
playerctl_status=$(playerctl --all-players status 2>/dev/null | grep -q "Playing" && echo 1 || echo 0)

# Se houver áudio, vídeo ou mídia sendo reproduzida, não suspende
if [ "$audio_playing" -gt 0 ] || [ "$video_playing" -gt 0 ] || [ "$playerctl_status" -eq 1 ]; then
    echo "Mídia detectada, não suspendendo o sistema."
    exit 0
fi

# Bloqueia a tela antes de suspender
swaylock -f -c 000000 &

# Suspende o sistema e aguarda
echo "Sem mídia detectada, suspendendo o sistema."
systemctl suspend

