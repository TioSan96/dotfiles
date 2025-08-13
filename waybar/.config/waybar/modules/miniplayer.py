#!/usr/bin/env python3
import subprocess
import json

def get_info(cmd):
    try:
        return subprocess.check_output(cmd, shell=True).decode().strip()
    except:
        return ""

title = get_info("playerctl metadata title")
artist = get_info("playerctl metadata artist")
status = get_info("playerctl status")
player = get_info("playerctl -l | head -n1")

if title and artist:
    text = f"{artist} - {title}"
elif title:
    text = title
else:
    text = "Nenhuma música"

icon = "" if status == "Playing" else ""
tooltip = f"Player: {player}\nStatus: {status}"
print(json.dumps({"text": text, "icon": icon, "tooltip": tooltip}))
 