#!/usr/bin/env python3
import json
import subprocess
import sys

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

def main():
    """Retorna JSON indicando se o navegador está ativo"""
    browser_active = is_browser_active()
    active_window = get_active_window()
    
    print(json.dumps({
        "browser_active": browser_active,
        "active_window": active_window
    }))

if __name__ == "__main__":
    main() 