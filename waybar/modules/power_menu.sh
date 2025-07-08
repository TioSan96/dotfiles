#!/bin/bash

chosen=$(echo -e "⏻ Desligar\n Reiniciar\n Suspender\n Bloquear" | \
    wofi --dmenu --width 200 --height 200 --prompt "Power")

case "$chosen" in
    "⏻ Desligar") systemctl poweroff ;;
    " Reiniciar") systemctl reboot ;;
    " Suspender") systemctl suspend ;;
    " Bloquear") hyprlock ;;
esac 