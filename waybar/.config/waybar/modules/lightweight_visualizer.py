#!/usr/bin/env python3
import json
import subprocess
import time
import random
import math

def get_volume():
    """Obtém volume do PulseAudio"""
    try:
        result = subprocess.run(['pactl', 'get-sink-volume', '@DEFAULT_SINK@'], 
                              capture_output=True, text=True, timeout=1)
        
        if result.returncode == 0:
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

def is_music_playing():
    """Verifica se há música tocando"""
    try:
        result = subprocess.run(['playerctl', 'status'], capture_output=True, text=True, timeout=1)
        return 'Playing' in result.stdout
    except:
        return False

def create_lightweight_bars(volume):
    """Cria barras leves e otimizadas"""
    if volume < 5:
        return ['▁'] * 8
    
    bars = []
    current_time = time.time()
    
    for i in range(8):
        # Frequência simples baseada na posição
        freq = 1 + i * 0.3
        
        # Onda simples
        wave = math.sin(current_time * freq) * 0.3
        
        # Intensidade baseada no volume
        base_intensity = volume / 100.0
        
        # Combina volume com onda
        intensity = base_intensity + wave
        
        # Adiciona um pouco de aleatoriedade
        intensity += random.random() * 0.2
        intensity = min(1.0, max(0.0, intensity))
        
        # Converte para barra (menos níveis para melhor performance)
        if intensity > 0.7:
            bars.append('█')
        elif intensity > 0.5:
            bars.append('▇')
        elif intensity > 0.3:
            bars.append('▆')
        else:
            bars.append('▁')
    
    return bars

def get_music_info():
    """Obtém informações da música"""
    try:
        title_result = subprocess.run(['playerctl', 'metadata', 'title'], 
                                    capture_output=True, text=True, timeout=1)
        title = title_result.stdout.strip()
        artist_result = subprocess.run(['playerctl', 'metadata', 'artist'], 
                                     capture_output=True, text=True, timeout=1)
        artist = artist_result.stdout.strip()
        return title, artist
    except:
        return "", ""

def main():
    volume = get_volume()
    is_playing = is_music_playing()
    
    if is_playing and volume > 5:
        bars = create_lightweight_bars(volume)
        bars_text = ''.join(bars)
        
        title, artist = get_music_info()
        
        if title and artist:
            tooltip = f"🎵 {title}\n👤 {artist}\n🔊 Volume: {volume:.0f}%\n🎶 Visualizador"
        else:
            tooltip = f"🔊 Volume: {volume:.0f}%\n🎶 Visualizador"
        
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