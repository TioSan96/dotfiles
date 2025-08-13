#!/usr/bin/env python3
import json
import subprocess
import sys

def get_players():
    result = subprocess.run(['playerctl', '-l'], capture_output=True, text=True)
    if result.returncode != 0:
        return []
    return [p.strip() for p in result.stdout.splitlines() if p.strip()]

def get_player_status(player):
    try:
        status = subprocess.run(['playerctl', '-p', player, 'status'], capture_output=True, text=True, timeout=3).stdout.strip()
        return status
    except Exception:
        return None

def get_metadata(player, field):
    try:
        return subprocess.run(['playerctl', '-p', player, 'metadata', field], capture_output=True, text=True, timeout=3).stdout.strip()
    except Exception:
        return ''

def get_player_info():
    players = get_players()
    print(f"DEBUG: Players found: {players}", file=sys.stderr)
    
    # Prioridade: Brave > Spotify > qualquer outro
    priority = [p for p in players if 'brave' in p.lower()] + \
               [p for p in players if 'spotify' in p.lower()] + \
               [p for p in players if 'brave' not in p.lower() and 'spotify' not in p.lower()]
    
    print(f"DEBUG: Priority order: {priority}", file=sys.stderr)
    
    for player in priority:
        status = get_player_status(player)
        print(f"DEBUG: Player {player} status: {status}", file=sys.stderr)
        
        if status == 'Playing':
            title = get_metadata(player, 'title')
            artist = get_metadata(player, 'artist')
            print(f"DEBUG: Title: '{title}', Artist: '{artist}'", file=sys.stderr)
            
            if title and artist:
                display_text = f"{title} - {artist}"
            elif title:
                display_text = title
            elif artist:
                display_text = artist
            else:
                display_text = player
                
            if len(display_text) > 40:
                display_text = display_text[:37] + "..."
                
            player_class = "spotify" if 'spotify' in player.lower() else ("brave" if 'brave' in player.lower() else "media")
            print(f"DEBUG: Returning: {display_text}", file=sys.stderr)
            
            return {
                "text": display_text,
                "tooltip": f"{title} - {artist} ({player})",
                "class": player_class
            }
    return None

if __name__ == "__main__":
    info = get_player_info()
    if info:
        print(json.dumps(info))
    else:
        print(json.dumps({"text": "", "tooltip": "", "class": ""})) 