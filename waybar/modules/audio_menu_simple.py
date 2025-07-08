#!/usr/bin/env python3
import json
import subprocess
import sys
import os

def get_volume():
    """Obtém volume atual"""
    try:
        result = subprocess.run(['pactl', 'get-sink-volume', '@DEFAULT_SINK@'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if 'front-left:' in line:
                    parts = line.split()
                    volume_str = parts[2]
                    volume = int(volume_str) / 65536 * 100
                    return int(volume)
        return 0
    except:
        return 0

def is_muted():
    """Verifica se está mutado"""
    try:
        result = subprocess.run(['pactl', 'get-sink-mute', '@DEFAULT_SINK@'], 
                              capture_output=True, text=True)
        return 'yes' in result.stdout.lower()
    except:
        return False

def get_audio_devices():
    """Obtém lista de dispositivos de áudio"""
    try:
        result = subprocess.run(['pactl', 'list', 'sinks', 'short'], 
                              capture_output=True, text=True)
        devices = []
        for line in result.stdout.strip().split('\n'):
            if line.strip():
                parts = line.split('\t')
                if len(parts) >= 2:
                    device_id = parts[0]
                    device_name = parts[1]
                    devices.append({
                        'id': device_id,
                        'name': device_name
                    })
        return devices
    except:
        return []

def get_current_device():
    """Obtém o dispositivo de áudio atual"""
    try:
        result = subprocess.run(['pactl', 'get-default-sink'], 
                              capture_output=True, text=True)
        return result.stdout.strip()
    except:
        return ""

def get_music_info():
    """Obtém informações da música atual"""
    try:
        status_result = subprocess.run(['playerctl', 'status'], 
                                     capture_output=True, text=True)
        if 'Playing' not in status_result.stdout:
            return None
        
        title_result = subprocess.run(['playerctl', 'metadata', 'title'], 
                                    capture_output=True, text=True)
        artist_result = subprocess.run(['playerctl', 'metadata', 'artist'], 
                                     capture_output=True, text=True)
        
        title = title_result.stdout.strip()
        artist = artist_result.stdout.strip()
        
        return {
            'title': title,
            'artist': artist
        }
    except:
        return None

def show_audio_menu():
    """Mostra menu de áudio usando wofi"""
    volume = get_volume()
    muted = is_muted()
    devices = get_audio_devices()
    current_device = get_current_device()
    music_info = get_music_info()
    
    # Cria as opções do menu
    menu_options = []
    
    # Seção de volume
    mute_status = "🔇 Mudo" if muted else "🔊 Não mudo"
    menu_options.append(f"🔊 Volume: {volume}% ({mute_status})")
    menu_options.append("")
    
    # Controles de volume
    menu_options.append("🔉 Diminuir volume (-10%)")
    menu_options.append("🔉 Diminuir volume (-5%)")
    menu_options.append("🔊 Aumentar volume (+5%)")
    menu_options.append("🔊 Aumentar volume (+10%)")
    menu_options.append("🔇 Alternar mute")
    menu_options.append("")
    
    # Seção de música
    if music_info:
        menu_options.append(f"🎵 {music_info['title']}")
        menu_options.append(f"👤 {music_info['artist']}")
        menu_options.append("")
        menu_options.append("⏮️ Música anterior")
        menu_options.append("⏯️ Play/Pause")
        menu_options.append("⏭️ Próxima música")
        menu_options.append("")
    
    # Seção de dispositivos
    if devices:
        menu_options.append("🎧 Dispositivos de Áudio:")
        for device in devices:
            is_current = device['id'] == current_device
            status = "✅" if is_current else "⚪"
            menu_options.append(f"{status} {device['name']}")
        menu_options.append("")
    
    # Opções de configuração
    menu_options.append("⚙️ Abrir pavucontrol")
    menu_options.append("🎛️ Abrir alsamixer")
    
    # Salva as opções em um arquivo temporário
    menu_file = "/tmp/waybar_audio_menu.txt"
    with open(menu_file, 'w') as f:
        for option in menu_options:
            f.write(option + '\n')
    
    # Mostra o menu usando wofi
    try:
        result = subprocess.run(['wofi', '--show', 'dmenu', '--prompt', 'Áudio', 
                               '--style', '/tmp/waybar_audio_menu.txt'], 
                              capture_output=True, text=True, input='\n'.join(menu_options))
        
        selected = result.stdout.strip()
        handle_menu_selection(selected, devices, current_device)
        
    except Exception as e:
        print(f"Erro ao mostrar menu: {e}")

def handle_menu_selection(selection, devices, current_device):
    """Processa a seleção do menu"""
    if not selection:
        return
    
    if "Diminuir volume (-10%)" in selection:
        subprocess.run(['pactl', 'set-sink-volume', '@DEFAULT_SINK@', '-10%'])
    elif "Diminuir volume (-5%)" in selection:
        subprocess.run(['pactl', 'set-sink-volume', '@DEFAULT_SINK@', '-5%'])
    elif "Aumentar volume (+5%)" in selection:
        subprocess.run(['pactl', 'set-sink-volume', '@DEFAULT_SINK@', '+5%'])
    elif "Aumentar volume (+10%)" in selection:
        subprocess.run(['pactl', 'set-sink-volume', '@DEFAULT_SINK@', '+10%'])
    elif "Alternar mute" in selection:
        subprocess.run(['pactl', 'set-sink-mute', '@DEFAULT_SINK@', 'toggle'])
    elif "Música anterior" in selection:
        subprocess.run(['playerctl', 'previous'])
    elif "Play/Pause" in selection:
        subprocess.run(['playerctl', 'play-pause'])
    elif "Próxima música" in selection:
        subprocess.run(['playerctl', 'next'])
    elif "Abrir pavucontrol" in selection:
        subprocess.run(['pavucontrol'])
    elif "Abrir alsamixer" in selection:
        subprocess.run(['kitty', '--hold', 'alsamixer'])
    else:
        # Verifica se é um dispositivo de áudio
        for device in devices:
            if device['name'] in selection and device['id'] != current_device:
                subprocess.run(['pactl', 'set-default-sink', device['id']])
                break

def main():
    """Função principal"""
    if len(sys.argv) > 1 and sys.argv[1] == "--menu":
        # Mostra o menu
        show_audio_menu()
    else:
        # Retorna informações básicas para o tooltip
        volume = get_volume()
        muted = is_muted()
        music_info = get_music_info()
        
        # Ícone baseado no volume e mute
        if muted:
            icon = "🔇"
        elif volume == 0:
            icon = "🔇"
        elif volume < 30:
            icon = "🔈"
        elif volume < 70:
            icon = "🔉"
        else:
            icon = "🔊"
        
        tooltip_text = f"{icon} Volume: {volume}%"
        if muted:
            tooltip_text += " (Mudo)"
        
        if music_info:
            tooltip_text += f"\n🎵 {music_info['title']}\n👤 {music_info['artist']}"
        
        print(json.dumps({
            "text": f"{icon} {volume}%",
            "tooltip": tooltip_text,
            "class": "audio-menu-trigger",
            "alt": "audio"
        }))

if __name__ == "__main__":
    main() 