#!/usr/bin/env python3

import json
import subprocess
import sys
import os
import re

def get_volume():
    try:
        result = subprocess.run(['pactl', 'get-sink-volume', '@DEFAULT_SINK@'], capture_output=True, text=True, check=True)
        output = result.stdout
        volume_str = output.split('%')[0].split('/')[-1].strip()
        return int(volume_str)
    except:
        return 0

def get_muted():
    try:
        result = subprocess.run(['pactl', 'get-sink-mute', '@DEFAULT_SINK@'], capture_output=True, text=True, check=True)
        return 'yes' in result.stdout.lower()
    except:
        return False

def get_sink_description():
    try:
        result = subprocess.run(['pactl', 'list', 'sinks'], capture_output=True, text=True, check=True)
        sinks = result.stdout.split('Sink #')
        for sink in sinks:
            if '@DEFAULT_SINK@' in sink or 'State: RUNNING' in sink:
                match = re.search(r'Description: (.+)', sink)
                if match:
                    return match.group(1)
        # fallback: pega o primeiro Description
        match = re.search(r'Description: (.+)', result.stdout)
        if match:
            return match.group(1)
    except:
        pass
    return "Dispositivo desconhecido"

def get_icon(volume, muted):
    # Usa ícones Nerd Font padrão Waybar
    if muted or volume == 0:
        return "<span color='#f7768e'></span>"  # Muted
    elif volume < 25:
        return "<span color='#7aa2f7'></span>"  # Baixo
    elif volume < 50:
        return "<span color='#7aa2f7'></span>"  # Médio
    else:
        return "<span color='#7aa2f7'></span>"  # Alto

def create_volume_bar(volume, width=12):
    filled = int((volume / 100) * width)
    empty = width - filled
    bar_filled = "█"
    bar_empty = "░"
    if volume < 30:
        color = "#f7768e"
    elif volume < 70:
        color = "#e0af68"
    else:
        color = "#9ece6a"
    bar = bar_filled * filled + bar_empty * empty
    return f"<span color='{color}'>{bar}</span>"

def set_bar_visible():
    # Garante que a barra fique visível
    toggle_file = "/tmp/waybar_volume_toggle"
    if not os.path.exists(toggle_file):
        with open(toggle_file, 'w') as f:
            f.write('1')

def main():
    # Se for scroll, manter barra visível
    if len(sys.argv) > 1 and sys.argv[1] == "--showbar":
        set_bar_visible()
        return
    if len(sys.argv) > 1 and sys.argv[1] == "--toggle":
        toggle_file = "/tmp/waybar_volume_toggle"
        if os.path.exists(toggle_file):
            os.remove(toggle_file)
        else:
            with open(toggle_file, 'w') as f:
                f.write('1')
        return
    volume = get_volume()
    muted = get_muted()
    sink_desc = get_sink_description()
    show_bar = os.path.exists("/tmp/waybar_volume_toggle")
    icon = get_icon(volume, muted)
    if muted:
        text = f"{icon} <span color='#f7768e'>Mudo</span>"
        tooltip = f" Áudio mutado\n📱 Dispositivo: {sink_desc}"
    else:
        if show_bar:
            bar = create_volume_bar(volume)
            text = f"{icon} <span color='#F1F1F1'>{volume}%</span> {bar}"
        else:
            text = f"{icon} <span color='#F1F1F1'>{volume}%</span>"
        tooltip = f" Volume: {volume}%\n📱 Dispositivo: {sink_desc}\n🖱️ Clique para alternar barra\n🖱️ Scroll para ajustar"
    output = {
        "text": text,
        "tooltip": tooltip,
        "class": "volume-control",
        "alt": "muted" if muted else "unmuted"
    }
    print(json.dumps(output))

if __name__ == "__main__":
    main() 