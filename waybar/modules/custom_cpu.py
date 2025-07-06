#!/usr/bin/python3
import json
import psutil
import os

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

# Monta o JSON para a Waybar
mode = get_mode()
if mode == 'percent':
    text = cpu_percent()
    tooltip = 'Clique para ver gráfico por núcleo'
else:
    text = cpu_graph()
    tooltip = 'Clique para ver porcentagem total'

print(json.dumps({
    'text': text,
    'tooltip': tooltip,
    'class': 'cpu-graph' if mode == 'graph' else ''
}))
