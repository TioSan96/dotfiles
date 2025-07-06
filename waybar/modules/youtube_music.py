#!/usr/bin/env python3
import json
import subprocess
import sys
import re
import time
import os

def get_players():
    """Lista todos os players MPRIS disponíveis"""
    try:
        result = subprocess.run(['playerctl', '-l'], capture_output=True, text=True)
        return result.stdout.strip().split('\n') if result.stdout.strip() else []
    except:
        return []

def get_metadata(player):
    """Obtém metadados de um player específico"""
    try:
        # Obtém título
        title_result = subprocess.run(['playerctl', '-p', player, 'metadata', 'title'], 
                                    capture_output=True, text=True)
        title = title_result.stdout.strip()
        
        # Obtém artista
        artist_result = subprocess.run(['playerctl', '-p', player, 'metadata', 'artist'], 
                                     capture_output=True, text=True)
        artist = artist_result.stdout.strip()
        
        # Obtém status (playing, paused, stopped)
        status_result = subprocess.run(['playerctl', '-p', player, 'status'], 
                                     capture_output=True, text=True)
        status = status_result.stdout.strip()
        
        return {
            'title': title,
            'artist': artist,
            'status': status,
            'player': player
        }
    except:
        return None

def is_youtube_music(player):
    """Verifica se o player é do Brave tocando música"""
    try:
        # Se é Brave e está tocando, vamos aceitar
        if 'brave' in player.lower():
            status_result = subprocess.run(['playerctl', '-p', player, 'status'], 
                                         capture_output=True, text=True)
            status = status_result.stdout.strip()
            
            # Se está tocando, aceita como válido
            if status == 'Playing':
                return True
                
        return False
    except:
        return False

def format_title(title, artist):
    """Formata o título para exibição"""
    if not title:
        return "Sem música"
    
    # Remove caracteres especiais do YouTube
    title = re.sub(r'\(Official.*?\)', '', title)
    title = re.sub(r'\[Official.*?\]', '', title)
    title = re.sub(r'\(Lyrics.*?\)', '', title)
    title = re.sub(r'\[Lyrics.*?\]', '', title)
    title = re.sub(r'\(Audio.*?\)', '', title)
    title = re.sub(r'\[Audio.*?\]', '', title)
    
    return title

def create_marquee_text(text, max_length=40):
    """Cria texto deslizante se for muito longo"""
    if len(text) <= max_length:
        return text
    
    # Arquivo para armazenar a posição do marquee
    marquee_file = "/tmp/waybar_marquee_pos"
    
    # Lê a posição atual
    try:
        with open(marquee_file, 'r') as f:
            pos = int(f.read().strip())
    except:
        pos = 0
    
    # Calcula nova posição (desliza a cada 2 segundos)
    current_time = int(time.time())
    pos = (current_time // 2) % (len(text) + 10)
    
    # Salva a nova posição
    with open(marquee_file, 'w') as f:
        f.write(str(pos))
    
    # Cria o texto deslizante
    if pos < len(text):
        display_text = text[pos:pos + max_length]
        if len(display_text) < max_length:
            # Adiciona espaços no final para completar
            display_text += " " * (max_length - len(display_text))
    else:
        # Volta ao início
        display_text = text[:max_length]
    
    return display_text

def main():
    players = get_players()
    youtube_music_data = None
    
    # Procura por Brave tocando música
    for player in players:
        if is_youtube_music(player):
            metadata = get_metadata(player)
            if metadata and metadata['status'] == 'Playing':
                youtube_music_data = metadata
                break
    
    if youtube_music_data:
        title = format_title(youtube_music_data['title'], youtube_music_data['artist'])
        artist = youtube_music_data['artist'] or "YouTube Music"
        
        # Cria o texto completo
        full_text = f"🎵 {title}"
        if artist and artist != "YouTube Music":
            full_text += f" - {artist}"
        
        # Aplica efeito marquee se necessário
        display_text = create_marquee_text(full_text, 50)
        
        # Tooltip com informações completas
        tooltip = f"🎵 {youtube_music_data['title']}\n👤 {artist}\n▶️ Tocando no Brave"
        
        print(json.dumps({
            "text": display_text,
            "tooltip": tooltip,
            "class": "youtube-music",
            "alt": "playing"
        }))
    else:
        print(json.dumps({
            "text": "",
            "tooltip": "YouTube Music não está tocando",
            "class": "",
            "alt": "stopped"
        }))

if __name__ == "__main__":
    main() 