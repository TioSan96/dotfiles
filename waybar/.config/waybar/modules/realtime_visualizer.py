#!/usr/bin/env python3
import json
import subprocess
import time
import random
import math

def get_real_audio_data():
    """Obtém dados reais de áudio do PulseAudio"""
    try:
        # Obtém volume atual
        result = subprocess.run(['pactl', 'get-sink-volume', '@DEFAULT_SINK@'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            # Extrai o volume
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if 'front-left:' in line:
                    parts = line.split()
                    volume_str = parts[2]
                    volume = int(volume_str) / 65536 * 100
                    return volume
        return 0
    except:
        return 0

def get_audio_activity():
    """Detecta atividade de áudio baseada em mudanças de volume"""
    try:
        # Obtém informações do sink
        result = subprocess.run(['pactl', 'list', 'sinks', 'short'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if '@DEFAULT_SINK@' in line:
                    parts = line.split()
                    if len(parts) >= 4:
                        # Verifica se está ativo
                        return parts[3] == 'RUNNING'
        return False
    except:
        return False

def create_realtime_bars(volume, is_active):
    """Cria barras baseadas em dados reais de áudio"""
    if not is_active or volume < 5:
        return ['▁'] * 8
    
    bars = []
    base_intensity = volume / 100.0
    
    for i in range(8):
        # Usa o tempo atual para criar variação
        current_time = time.time()
        
        # Combina volume real com variação temporal
        time_variation = math.sin(current_time * (2 + i * 0.5)) * 0.3
        random_factor = random.random() * 0.2
        
        # Intensidade baseada no volume real
        intensity = base_intensity + time_variation + random_factor
        intensity = min(1.0, max(0.0, intensity))
        
        # Converte para barra
        if intensity > 0.8:
            bars.append('█')
        elif intensity > 0.6:
            bars.append('▇')
        elif intensity > 0.4:
            bars.append('▆')
        elif intensity > 0.2:
            bars.append('▅')
        else:
            bars.append('▁')
    
    return bars

def is_music_playing():
    """Verifica se há música tocando"""
    try:
        result = subprocess.run(['playerctl', 'status'], capture_output=True, text=True)
        return 'Playing' in result.stdout
    except:
        return False

def main():
    volume = get_real_audio_data()
    is_active = get_audio_activity()
    is_playing = is_music_playing()
    
    if is_playing and is_active:
        bars = create_realtime_bars(volume, is_active)
        bars_text = ''.join(bars)
        
        # Obtém informações da música
        try:
            title_result = subprocess.run(['playerctl', 'metadata', 'title'], 
                                        capture_output=True, text=True)
            title = title_result.stdout.strip()
            artist_result = subprocess.run(['playerctl', 'metadata', 'artist'], 
                                         capture_output=True, text=True)
            artist = artist_result.stdout.strip()
            
            if title and artist:
                tooltip = f"🎵 {title}\n👤 {artist}\n🔊 Volume: {volume:.0f}%\n🎶 Tempo Real"
            else:
                tooltip = f"🔊 Volume: {volume:.0f}%\n🎶 Visualizador Tempo Real"
        except:
            tooltip = f"🔊 Volume: {volume:.0f}%\n🎶 Visualizador Tempo Real"
        
        print(json.dumps({
            "text": f"🎵 {bars_text}",
            "tooltip": tooltip,
            "class": "audio-visualizer",
            "alt": "playing"
        }))
    else:
        print(json.dumps({
            "text": "",
            "tooltip": "Nenhum áudio ativo",
            "class": "",
            "alt": "stopped"
        }))

if __name__ == "__main__":
    main() 