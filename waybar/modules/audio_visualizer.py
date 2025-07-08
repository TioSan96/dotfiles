#!/usr/bin/env python3
import json
import subprocess
import time
import random

def get_audio_level():
    """Simula nível de áudio baseado na atividade do sistema"""
    try:
        # Verifica se há áudio tocando
        result = subprocess.run(['playerctl', 'status'], capture_output=True, text=True)
        if 'Playing' in result.stdout:
            # Se está tocando, gera barras animadas
            return True
        return False
    except:
        return False

def create_visualizer_bars(is_playing):
    """Cria barras de visualização"""
    if not is_playing:
        return "▁▂▃▄▅▆▇█"
    
    # Gera barras aleatórias para simular visualização
    bars = []
    for _ in range(8):
        if random.random() > 0.3:  # 70% chance de barra alta
            bars.append(random.choice(['▅', '▆', '▇', '█']))
        else:
            bars.append(random.choice(['▁', '▂', '▃', '▄']))
    
    return ''.join(bars)

def main():
    is_playing = get_audio_level()
    bars = create_visualizer_bars(is_playing)
    
    if is_playing:
        print(json.dumps({
            "text": f"🎵 {bars}",
            "tooltip": "Visualizador de Áudio Ativo",
            "class": "audio-visualizer",
            "alt": "playing"
        }))
    else:
        print(json.dumps({
            "text": "",
            "tooltip": "Nenhum áudio tocando",
            "class": "",
            "alt": "stopped"
        }))

if __name__ == "__main__":
    main() 