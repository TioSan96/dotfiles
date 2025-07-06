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
                              capture_output=True, text=True)
        
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
        result = subprocess.run(['playerctl', 'status'], capture_output=True, text=True)
        return 'Playing' in result.stdout
    except:
        return False

def create_dynamic_bars(volume):
    """Cria barras dinâmicas que reagem à música"""
    if volume < 5:
        return ['▁'] * 8
    
    bars = []
    current_time = time.time()
    
    for i in range(8):
        # Frequências mais altas para movimento mais rápido
        freq1 = 3 + i * 1.2  # Onda principal
        freq2 = 5 + i * 0.8  # Onda secundária
        freq3 = 2 + i * 0.5  # Onda de baixa frequência
        
        # Combina múltiplas ondas
        wave1 = math.sin(current_time * freq1) * 0.3
        wave2 = math.sin(current_time * freq2) * 0.2
        wave3 = math.sin(current_time * freq3) * 0.4
        
        # Intensidade baseada no volume
        base_intensity = volume / 100.0
        
        # Combina todas as ondas
        total_wave = wave1 + wave2 + wave3
        intensity = base_intensity + total_wave
        
        # Adiciona variação baseada na posição
        position_factor = 1 + (i * 0.1)
        intensity *= position_factor
        
        # Adiciona ruído aleatório
        noise = random.random() * 0.3
        intensity += noise
        
        # Normaliza
        intensity = min(1.0, max(0.0, intensity))
        
        # Converte para barra com mais níveis
        if intensity > 0.9:
            bars.append('█')
        elif intensity > 0.75:
            bars.append('▇')
        elif intensity > 0.6:
            bars.append('▆')
        elif intensity > 0.45:
            bars.append('▅')
        elif intensity > 0.3:
            bars.append('▄')
        elif intensity > 0.15:
            bars.append('▃')
        else:
            bars.append('▁')
    
    return bars

def get_music_info():
    """Obtém informações da música"""
    try:
        title_result = subprocess.run(['playerctl', 'metadata', 'title'], 
                                    capture_output=True, text=True)
        title = title_result.stdout.strip()
        artist_result = subprocess.run(['playerctl', 'metadata', 'artist'], 
                                     capture_output=True, text=True)
        artist = artist_result.stdout.strip()
        return title, artist
    except:
        return "", ""

def main():
    volume = get_volume()
    is_playing = is_music_playing()
    
    if is_playing and volume > 5:
        bars = create_dynamic_bars(volume)
        bars_text = ''.join(bars)
        
        title, artist = get_music_info()
        
        if title and artist:
            tooltip = f"🎵 {title}\n👤 {artist}\n🔊 Volume: {volume:.0f}%\n🎶 Visualizador Dinâmico"
        else:
            tooltip = f"🔊 Volume: {volume:.0f}%\n🎶 Visualizador Dinâmico"
        
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