#!/usr/bin/python3
import json
import psutil
import os
import time
import re

STATE_FILE = '/tmp/waybar_cpu_mode'

# Função para ler o modo atual (porcentagem ou gráfico)
def get_mode():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            mode = f.read().strip()
            if mode in ['percent', 'graph']:
                return mode
    return 'percent'

# Função para alternar o modo
def toggle_mode():
    mode = get_mode()
    new_mode = 'graph' if mode == 'percent' else 'percent'
    with open(STATE_FILE, 'w') as f:
        f.write(new_mode)

# Se for chamado com argumento --toggle, alterna o modo e sai
import sys
if len(sys.argv) > 1 and sys.argv[1] == '--toggle':
    toggle_mode()
    sys.exit(0)

# Gera o gráfico de barras por núcleo
def cpu_graph():
    bars = '▁▂▃▄▅▆▇█'
    percs = psutil.cpu_percent(percpu=True)
    graph = ''.join(bars[min(int(p/12.5), 7)] for p in percs)
    return graph

# Mostra o uso total em porcentagem
def cpu_percent():
    return f"<span color='#7aa2f7'></span> {psutil.cpu_percent():.0f}%"

# Obtém informações detalhadas da CPU
def get_cpu_details():
    cpu_percent_total = psutil.cpu_percent()
    cpu_percent_per_core = psutil.cpu_percent(percpu=True)
    cpu_freq = psutil.cpu_freq()
    cpu_count = psutil.cpu_count()
    cpu_count_logical = psutil.cpu_count(logical=True)
    load_avg = psutil.getloadavg()
    
    # Informações do modelo da CPU
    try:
        with open('/proc/cpuinfo', 'r') as f:
            cpuinfo = f.read()
            model_match = re.search(r'model name\s+:\s+(.+)', cpuinfo)
            cpu_model = model_match.group(1) if model_match else "CPU Desconhecida"
    except:
        cpu_model = "CPU Desconhecida"
    
    # Top processos por CPU
    try:
        processes = []
        for proc in sorted(psutil.process_iter(['pid', 'name', 'cpu_percent']), 
                          key=lambda x: x.info['cpu_percent'], reverse=True)[:5]:
            if proc.info['cpu_percent'] > 0:
                processes.append({
                    'name': proc.info['name'][:20],
                    'cpu': proc.info['cpu_percent'],
                    'pid': proc.info['pid']
                })
    except:
        processes = []
    
    return {
        'total': cpu_percent_total,
        'per_core': cpu_percent_per_core,
        'freq': cpu_freq.current if cpu_freq else 0,
        'cores': cpu_count,
        'threads': cpu_count_logical,
        'load_avg': load_avg,
        'model': cpu_model,
        'processes': processes
    }

# Cria tooltip avançado
def create_advanced_tooltip():
    details = get_cpu_details()
    
    # Gráfico por núcleo
    bars = '▁▂▃▄▅▆▇█'
    core_graph = ''.join(bars[min(int(p/12.5), 7)] for p in details['per_core'])
    
    # Informações básicas
    tooltip = f"""CPU: {details['total']:.1f}%
Nucleos: {details['cores']} fisicos, {details['threads']} logicos
Frequencia: {details['freq']/1000:.1f} GHz
Load Average: {details['load_avg'][0]:.2f}, {details['load_avg'][1]:.2f}, {details['load_avg'][2]:.2f}

Uso por Nucleo:
{core_graph}

Top Processos:"""
    
    # Adiciona processos
    for i, proc in enumerate(details['processes'], 1):
        tooltip += f"\n{i}. {proc['name']} ({proc['cpu']:.1f}%)"
    
    if not details['processes']:
        tooltip += "\nNenhum processo ativo"
    
    tooltip += f"\n\nClique para alternar visualizacao"
    
    return tooltip

# Monta o JSON para a Waybar
mode = get_mode()
if mode == 'percent':
    text = cpu_percent()
    tooltip = create_advanced_tooltip()
else:
    text = cpu_graph()
    tooltip = create_advanced_tooltip()

print(json.dumps({
    'text': text,
    'tooltip': tooltip,
    'class': 'cpu-graph' if mode == 'graph' else ''
}))
