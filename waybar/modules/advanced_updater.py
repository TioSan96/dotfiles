#!/usr/bin/env python3

import json
import subprocess
import os
import time
import re
from datetime import datetime

def run_command(cmd):
    """Executa comando e retorna resultado"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return result.stdout.strip()
    except:
        return ""

def get_package_size(package_name):
    """Obtém o tamanho aproximado do pacote"""
    try:
        # Tenta obter informações do pacote
        info = run_command(f"pacman -Si {package_name} 2>/dev/null")
        if info:
            size_match = re.search(r'Installed Size\s+:\s+([\d.]+)\s+(\w+)', info)
            if size_match:
                return f"{size_match.group(1)} {size_match.group(2)}"
    except:
        pass
    return "N/A"

def get_critical_packages():
    """Lista pacotes críticos (kernel, segurança)"""
    critical = []
    try:
        # Verifica atualizações do kernel
        kernel_updates = run_command("checkupdates | grep -E '(linux|linux-zen|linux-lts)'")
        if kernel_updates:
            critical.extend(kernel_updates.split('\n'))
        
        # Verifica atualizações de segurança
        security_updates = run_command("checkupdates | grep -E '(openssl|firefox|chromium|brave)'")
        if security_updates:
            critical.extend(security_updates.split('\n'))
    except:
        pass
    return critical

def get_orphan_packages():
    """Obtém pacotes órfãos"""
    try:
        orphans = run_command("pacman -Qtdq")
        return len(orphans.split('\n')) if orphans else 0
    except:
        return 0

def get_disk_space():
    """Obtém espaço em disco disponível"""
    try:
        df = run_command("df -h /")
        lines = df.split('\n')
        if len(lines) > 1:
            parts = lines[1].split()
            if len(parts) >= 4:
                return parts[3]  # Espaço disponível
    except:
        pass
    return "N/A"

def get_last_update():
    """Obtém data da última atualização"""
    try:
        log_file = "/var/log/pacman.log"
        if os.path.exists(log_file):
            last_update = run_command(f"grep 'pacman -Syu' {log_file} | tail -1 | cut -d' ' -f1,2")
            if last_update:
                return last_update
    except:
        pass
    return "Desconhecida"

def check_updates():
    """Verifica todas as atualizações disponíveis"""
    updates = {
        'repositories': [],
        'aur': [],
        'flatpak': [],
        'critical': [],
        'total': 0
    }
    
    # Verifica repositórios
    try:
        repo_updates = run_command("checkupdates")
        if repo_updates:
            updates['repositories'] = [line.strip() for line in repo_updates.split('\n') if line.strip()]
    except:
        pass
    
    # Verifica AUR
    try:
        aur_updates = run_command("yay -Qu --aur")
        if aur_updates:
            updates['aur'] = [line.strip() for line in aur_updates.split('\n') if line.strip()]
    except:
        pass
    
    # Verifica Flatpak
    try:
        flatpak_updates = run_command("flatpak remote-ls --updates")
        if flatpak_updates:
            updates['flatpak'] = [line.strip() for line in flatpak_updates.split('\n') if line.strip()]
    except:
        pass
    
    # Calcula total
    updates['total'] = len(updates['repositories']) + len(updates['aur']) + len(updates['flatpak'])
    
    # Identifica pacotes críticos
    updates['critical'] = get_critical_packages()
    
    return updates

def create_advanced_tooltip(updates):
    """Cria tooltip avançado com informações detalhadas"""
    if updates['total'] == 0:
        return "Sistema atualizado"
    
    tooltip = f"Atualizacoes Disponiveis: {updates['total']}\n"
    tooltip += f"Ultima atualizacao: {get_last_update()}\n"
    tooltip += f"Espaco disponivel: {get_disk_space()}\n"
    
    orphan_count = get_orphan_packages()
    if orphan_count > 0:
        tooltip += f"Pacotes orfaos: {orphan_count}\n"
    
    tooltip += "\nDetalhes:\n"
    
    # Repositórios
    if updates['repositories']:
        tooltip += f"\nRepositorios ({len(updates['repositories'])}):\n"
        for i, pkg in enumerate(updates['repositories'][:5], 1):
            pkg_name = pkg.split()[0] if pkg else ""
            size = get_package_size(pkg_name)
            tooltip += f"{i}. {pkg_name} ({size})\n"
        if len(updates['repositories']) > 5:
            tooltip += f"... e mais {len(updates['repositories']) - 5}\n"
    
    # AUR
    if updates['aur']:
        tooltip += f"\nAUR ({len(updates['aur'])}):\n"
        for i, pkg in enumerate(updates['aur'][:5], 1):
            pkg_name = pkg.split()[0] if pkg else ""
            tooltip += f"{i}. {pkg_name}\n"
        if len(updates['aur']) > 5:
            tooltip += f"... e mais {len(updates['aur']) - 5}\n"
    
    # Flatpak
    if updates['flatpak']:
        tooltip += f"\nFlatpak ({len(updates['flatpak'])}):\n"
        for i, pkg in enumerate(updates['flatpak'][:5], 1):
            pkg_name = pkg.split()[0] if pkg else ""
            tooltip += f"{i}. {pkg_name}\n"
        if len(updates['flatpak']) > 5:
            tooltip += f"... e mais {len(updates['flatpak']) - 5}\n"
    
    # Pacotes críticos
    if updates['critical']:
        tooltip += f"\nPacotes Criticos:\n"
        for pkg in updates['critical'][:3]:
            tooltip += f"⚠ {pkg}\n"
    
    tooltip += "\nClique para atualizar"
    
    return tooltip

def main():
    updates = check_updates()
    
    if updates['total'] > 0:
        text = f"{updates['total']}"
        tooltip = create_advanced_tooltip(updates)
        class_name = "updates-available"
    else:
        text = ""
        tooltip = "Sistema atualizado"
        class_name = "system-updated"
    
    output = {
        "text": text,
        "tooltip": tooltip,
        "class": class_name
    }
    
    print(json.dumps(output))

if __name__ == "__main__":
    main() 