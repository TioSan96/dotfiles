#!/usr/bin/python3
import json
import psutil
import os

STATE_FILE = '/tmp/waybar_memory_mode'

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

# Gera o gráfico de barras de uso de memória
def memory_graph():
    bars = '▁▂▃▄▅▆▇█'
    memory = psutil.virtual_memory()
    percent = memory.percent
    # Divide em 8 barras para representar o uso
    bar_index = min(int(percent / 12.5), 7)
    graph = bars[bar_index] * 8  # Repete a barra 8 vezes para visual
    return graph

# Mostra o uso de memória em porcentagem
def memory_percent():
    memory = psutil.virtual_memory()
    return f"<span color='#7aa2f7'>💾</span> {memory.percent:.0f}%"

# Monta o JSON para a Waybar
mode = get_mode()
if mode == 'percent':
    text = memory_percent()
    tooltip = 'Clique para ver gráfico de uso'
else:
    text = memory_graph()
    tooltip = 'Clique para ver porcentagem'

print(json.dumps({
    'text': text,
    'tooltip': tooltip,
    'class': 'memory-graph' if mode == 'graph' else ''
})) 