#!/usr/bin/python3
import json
import psutil
import os
import time

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
    return f"<span color='#7aa2f7'>󰍛</span> {memory.percent:.0f}%"

# Obtém informações detalhadas de memória
def get_memory_details():
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    
    # Converte bytes para GB
    def bytes_to_gb(bytes_value):
        return bytes_value / (1024**3)
    
    # Top processos por memória
    try:
        processes = []
        for proc in sorted(psutil.process_iter(['pid', 'name', 'memory_info']), 
                          key=lambda x: x.info['memory_info'].rss, reverse=True)[:5]:
            if proc.info['memory_info'].rss > 0:
                processes.append({
                    'name': proc.info['name'][:20],
                    'memory_mb': proc.info['memory_info'].rss / (1024**2),
                    'pid': proc.info['pid']
                })
    except:
        processes = []
    
    return {
        'total_gb': bytes_to_gb(memory.total),
        'used_gb': bytes_to_gb(memory.used),
        'available_gb': bytes_to_gb(memory.available),
        'free_gb': bytes_to_gb(memory.free),
        'percent': memory.percent,
        'swap_total_gb': bytes_to_gb(swap.total),
        'swap_used_gb': bytes_to_gb(swap.used),
        'swap_percent': swap.percent,
        'processes': processes
    }

# Cria barra visual de progresso
def create_memory_bar(percent, width=20):
    filled = int((percent / 100) * width)
    empty = width - filled
    
    if percent < 50:
        color = "#9ece6a"  # Verde
    elif percent < 80:
        color = "#e0af68"  # Amarelo
    else:
        color = "#f7768e"  # Vermelho
    
    bar_filled = "█"
    bar_empty = "░"
    
    return f"<span color='{color}'>{bar_filled * filled}{bar_empty * empty}</span>"

# Cria tooltip avançado
def create_advanced_tooltip():
    details = get_memory_details()
    
    # Barra de progresso
    memory_bar = create_memory_bar(details['percent'])
    swap_bar = create_memory_bar(details['swap_percent']) if details['swap_total_gb'] > 0 else "N/A"
    
    # Informações básicas
    tooltip = f"""RAM: {details['percent']:.1f}%
Total: {details['total_gb']:.1f} GB
Usado: {details['used_gb']:.1f} GB
Livre: {details['free_gb']:.1f} GB
Disponivel: {details['available_gb']:.1f} GB

Barra de Uso:
{memory_bar}"""

    # Adiciona informações de swap se disponível
    if details['swap_total_gb'] > 0:
        tooltip += f"""

SWAP: {details['swap_percent']:.1f}%
Total: {details['swap_total_gb']:.1f} GB
Usado: {details['swap_used_gb']:.1f} GB

Barra de Swap:
{swap_bar}"""

    tooltip += f"""

Top Processos:"""
    
    # Adiciona processos
    for i, proc in enumerate(details['processes'], 1):
        tooltip += f"\n{i}. {proc['name']} ({proc['memory_mb']:.1f} MB)"
    
    if not details['processes']:
        tooltip += "\nNenhum processo ativo"
    
    tooltip += f"\n\nClique para alternar visualizacao"
    
    return tooltip

# Monta o JSON para a Waybar
mode = get_mode()
if mode == 'percent':
    text = memory_percent()
    tooltip = create_advanced_tooltip()
else:
    text = memory_graph()
    tooltip = create_advanced_tooltip()

print(json.dumps({
    'text': text,
    'tooltip': tooltip,
    'class': 'memory-graph' if mode == 'graph' else ''
})) 