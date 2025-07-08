#!/usr/bin/env python3
import json
import subprocess
import sys
import re
import time
import os

def get_active_window():
    """Obtém a janela ativa usando hyprctl"""
    try:
        result = subprocess.run(['hyprctl', 'activewindow'], capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if 'class:' in line:
                    return line.split(':')[1].strip()
        return None
    except:
        return None

def is_browser_active():
    """Verifica se um navegador está ativo"""
    active_window = get_active_window()
    if not active_window:
        return False
    
    # Lista de navegadores comuns (incluindo variações de classe)
    browsers = [
        'brave', 'firefox', 'chromium', 'google-chrome', 'microsoft-edge',
        'opera', 'vivaldi', 'safari', 'qutebrowser', 'falkon', 'konqueror',
        'brave-browser', 'firefox-esr', 'chromium-browser', 'chrome',
        'google-chrome-stable', 'microsoft-edge-stable'
    ]
    
    return any(browser in active_window.lower() for browser in browsers)

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

def main():
    # Verifica se o navegador está ativo
    browser_active = is_browser_active()
    
    # Se o navegador está ativo, oculta o módulo
    if browser_active:
        print(json.dumps({
            "text": "",
            "tooltip": "Oculto - Navegador ativo",
            "class": "hidden",
            "alt": "hidden"
        }))
        return
    
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
        
        # Cria o texto completo sem deslizamento
        full_text = f"🎵 {title}"
        if artist and artist != "YouTube Music":
            full_text += f" - {artist}"
        
        # Tooltip com informações completas
        tooltip = f"🎵 {youtube_music_data['title']}\n👤 {artist}\n▶️ Tocando no Brave"
        
        print(json.dumps({
            "text": full_text,
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