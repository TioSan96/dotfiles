#!/bin/bash

# Função para pegar o volume e o mute
get_sink_info() {
    local sink=$1
    # Pegando volume e mute do sink
    volume=$(pactl list sinks | grep -A 15 "Sink #$sink" | grep "Volume:" | head -n 1 | awk '{print $5}' | sed 's/%//')
    mute=$(pactl list sinks | grep -A 15 "Sink #$sink" | grep "Mute:" | awk '{print $2}')
}

# Função para mostrar a notificação
show_osd() {
    local sink=$1
    local volume=$2
    local mute=$3
    local icon=""
    local title="Volume - Output Device"
    local message="Volume: $volume%"

    if [[ "$mute" == "yes" || "$volume" -eq 0 ]]; then
        icon="audio-volume-muted"
        message="Muted"
    else
        if (( volume <= 33 )); then
            icon="audio-volume-low"
        elif (( volume <= 66 )); then
            icon="audio-volume-medium"
        else
            icon="audio-volume-high"
        fi
    fi

    # Exibe a notificação usando notify-send
    notify-send "$title" "$message" -i "$icon"
}

# Função para pegar o sink ativo
get_default_sink() {
    default_sink=$(pactl info | grep "Default Sink" | awk '{print $3}')
    echo $default_sink
}

# Script principal
sink=$(get_default_sink)
get_sink_info $sink
show_osd $sink $volume $mute
