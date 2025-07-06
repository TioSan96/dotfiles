#!/bin/bash

# Função para exibir a notificação OSD
function show_osd {
    local message=$1
    swaync -t 1 "$message"
}

# Verifica o parâmetro que foi passado
case "$1" in
    XF86AudioRaiseVolume)
        wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%+
        NEW_VOLUME=$(wpctl get-volume @DEFAULT_AUDIO_SINK@ | awk '{print $2}')
        show_osd "Volume: $NEW_VOLUME"
        ;;
    
    XF86AudioLowerVolume)
        wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-
        NEW_VOLUME=$(wpctl get-volume @DEFAULT_AUDIO_SINK@ | awk '{print $2}')
        show_osd "Volume: $NEW_VOLUME"
        ;;
    
    XF86AudioMute)
        wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle
        MUTE_STATUS=$(wpctl get-mute @DEFAULT_AUDIO_SINK@ | awk '{print $2}')
        show_osd "Mute: $MUTE_STATUS"
        ;;
    
    XF86AudioMicMute)
        wpctl set-mute @DEFAULT_AUDIO_SOURCE@ toggle
        MUTE_STATUS=$(wpctl get-mute @DEFAULT_AUDIO_SOURCE@ | awk '{print $2}')
        show_osd "Mic Mute: $MUTE_STATUS"
        ;;
    
    XF86MonBrightnessUp)
        brightnessctl s 10%+
        BRIGHTNESS=$(brightnessctl g)
        show_osd "Brightness: $BRIGHTNESS"
        ;;
    
    XF86MonBrightnessDown)
        brightnessctl s 10%-
        BRIGHTNESS=$(brightnessctl g)
        show_osd "Brightness: $BRIGHTNESS"
        ;;
    
    *)
        echo "Key not mapped!"
        ;;
esac
