#!/usr/bin/env python3
import json
import subprocess
import time
import random
import math
import threading
import os

class AudioVisualizer:
    def __init__(self):
        self.last_volume = 0
        self.volume_history = []
        self.peak_volume = 0
        self.is_active = False
        self.last_update = time.time()
        
    def get_volume_data(self):
        """Obtém dados de volume do PulseAudio"""
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
    
    def get_sink_status(self):
        """Verifica se o sink está ativo"""
        try:
            result = subprocess.run(['pactl', 'list', 'sinks', 'short'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if '@DEFAULT_SINK@' in line:
                        parts = line.split()
                        if len(parts) >= 4:
                            return parts[3] == 'RUNNING'
            return False
        except:
            return False
    
    def detect_audio_activity(self):
        """Detecta atividade de áudio baseada em mudanças de volume"""
        current_volume = self.get_volume_data()
        current_time = time.time()
        
        # Adiciona volume ao histórico
        self.volume_history.append(current_volume)
        if len(self.volume_history) > 10:
            self.volume_history.pop(0)
        
        # Calcula variação de volume
        if len(self.volume_history) > 1:
            volume_variation = max(self.volume_history) - min(self.volume_history)
        else:
            volume_variation = 0
        
        # Detecta atividade baseada em mudanças de volume
        is_active = self.get_sink_status() and volume_variation > 1
        
        # Atualiza pico de volume
        if current_volume > self.peak_volume:
            self.peak_volume = current_volume
        else:
            self.peak_volume *= 0.95  # Decaimento gradual
        
        self.last_volume = current_volume
        self.is_active = is_active
        self.last_update = current_time
        
        return current_volume, is_active, volume_variation
    
    def create_dynamic_bars(self, volume, is_active, variation):
        """Cria barras dinâmicas baseadas em dados reais"""
        if not is_active or volume < 5:
            return ['▁'] * 8
        
        bars = []
        current_time = time.time()
        
        # Base de intensidade do volume real
        base_intensity = volume / 100.0
        
        # Fator de atividade baseado na variação
        activity_factor = min(1.0, variation / 20.0)
        
        for i in range(8):
            # Frequência baseada na posição da barra
            freq = 1 + i * 0.8
            
            # Combina múltiplos fatores para criar movimento realista
            time_wave = math.sin(current_time * freq) * 0.4
            volume_wave = math.sin(current_time * freq * 0.5) * base_intensity * 0.3
            activity_wave = math.sin(current_time * freq * 1.2) * activity_factor * 0.5
            
            # Adiciona ruído baseado na atividade
            noise = random.random() * activity_factor * 0.3
            
            # Combina todos os fatores
            intensity = base_intensity + time_wave + volume_wave + activity_wave + noise
            intensity = min(1.0, max(0.0, intensity))
            
            # Aplica suavização baseada no pico de volume
            if self.peak_volume > 0:
                peak_factor = min(1.0, volume / self.peak_volume)
                intensity *= (0.7 + peak_factor * 0.3)
            
            # Converte para barra
            if intensity > 0.85:
                bars.append('█')
            elif intensity > 0.7:
                bars.append('▇')
            elif intensity > 0.55:
                bars.append('▆')
            elif intensity > 0.4:
                bars.append('▅')
            elif intensity > 0.25:
                bars.append('▃')
            else:
                bars.append('▁')
        
        return bars
    
    def is_music_playing(self):
        """Verifica se há música tocando"""
        try:
            result = subprocess.run(['playerctl', 'status'], capture_output=True, text=True)
            return 'Playing' in result.stdout
        except:
            return False
    
    def get_music_info(self):
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
    
    def generate_output(self):
        """Gera saída do visualizador"""
        volume, is_active, variation = self.detect_audio_activity()
        is_playing = self.is_music_playing()
        
        if is_playing and is_active:
            bars = self.create_dynamic_bars(volume, is_active, variation)
            bars_text = ''.join(bars)
            
            title, artist = self.get_music_info()
            
            if title and artist:
                tooltip = f"🎵 {title}\n👤 {artist}\n🔊 Volume: {volume:.0f}%\n📊 Atividade: {variation:.1f}\n🎶 Visualizador Avançado"
            else:
                tooltip = f"🔊 Volume: {volume:.0f}%\n📊 Atividade: {variation:.1f}\n🎶 Visualizador Avançado"
            
            return {
                "text": f"🎵 {bars_text}",
                "tooltip": tooltip,
                "class": "audio-visualizer",
                "alt": "playing"
            }
        else:
            return {
                "text": "",
                "tooltip": "Nenhum áudio ativo",
                "class": "",
                "alt": "stopped"
            }

def main():
    visualizer = AudioVisualizer()
    output = visualizer.generate_output()
    print(json.dumps(output))

if __name__ == "__main__":
    main() 