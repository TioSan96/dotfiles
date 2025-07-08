#!/usr/bin/env python3
import json
import subprocess
import sys
import os

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

def create_menu_html():
    """Cria o HTML do menu dropdown"""
    volume = get_volume()
    muted = is_muted()
    devices = get_audio_devices()
    current_device = get_current_device()
    music_info = get_music_info()
    
    html = f"""
    <div class="audio-menu">
        <div class="menu-header">
            <h3>🎵 Controles de Áudio</h3>
        </div>
        
        <div class="volume-section">
            <div class="volume-display">
                <span class="volume-icon">🔊</span>
                <span class="volume-text">{volume}%</span>
                <span class="mute-status">{'🔇' if muted else '🔊'}</span>
            </div>
            <div class="volume-controls">
                <button onclick="change_volume(-10)">-10%</button>
                <button onclick="change_volume(-5)">-5%</button>
                <button onclick="change_volume(5)">+5%</button>
                <button onclick="change_volume(10)">+10%</button>
            </div>
        </div>
    """
    
    if music_info:
        html += f"""
        <div class="music-section">
            <div class="music-info">
                <div class="music-title">🎵 {music_info['title']}</div>
                <div class="music-artist">👤 {music_info['artist']}</div>
            </div>
            <div class="music-controls">
                <button onclick="playerctl_previous()">⏮️</button>
                <button onclick="playerctl_play_pause()">⏯️</button>
                <button onclick="playerctl_next()">⏭️</button>
            </div>
        </div>
        """
    
    if devices:
        html += """
        <div class="devices-section">
            <h4>🎧 Dispositivos de Áudio</h4>
            <div class="device-list">
        """
        
        for device in devices:
            is_current = device['id'] == current_device
            status_icon = "✅" if is_current else "⚪"
            html += f"""
            <div class="device-item {('current' if is_current else '')}">
                <span class="device-icon">{status_icon}</span>
                <span class="device-name">{device['name']}</span>
                <button onclick="set_device('{device['id']}')" class="set-device-btn">
                    {('Atual' if is_current else 'Usar')}
                </button>
            </div>
            """
        
        html += """
            </div>
        </div>
        """
    
    html += """
        <div class="menu-footer">
            <button onclick="open_pavucontrol()">⚙️ Configurações</button>
            <button onclick="open_alsamixer()">🎛️ Mixer</button>
        </div>
    </div>
    """
    
    return html

def main():
    """Função principal"""
    if len(sys.argv) > 1 and sys.argv[1] == "--menu":
        # Retorna o HTML do menu
        print(create_menu_html())
    else:
        # Retorna informações básicas para o tooltip
        volume = get_volume()
        muted = is_muted()
        music_info = get_music_info()
        
        tooltip_text = f"🔊 Volume: {volume}%"
        if muted:
            tooltip_text += " (Mudo)"
        
        if music_info:
            tooltip_text += f"\n🎵 {music_info['title']}\n👤 {music_info['artist']}"
        
        print(json.dumps({
            "text": f"🔊 {volume}%",
            "tooltip": tooltip_text,
            "class": "audio-menu-trigger",
            "alt": "audio"
        }))

if __name__ == "__main__":
    main() 