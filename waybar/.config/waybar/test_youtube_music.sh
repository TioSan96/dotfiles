#!/bin/bash

echo "🎵 Testando detecção do YouTube Music no Brave..."
echo ""

# Teste 1: Listar todos os players
echo "1️⃣ Players disponíveis:"
playerctl -l
echo ""

# Teste 2: Verificar se Brave está na lista
echo "2️⃣ Verificando se Brave está na lista:"
if playerctl -l | grep -i brave; then
    echo "   ✅ Brave encontrado!"
else
    echo "   ❌ Brave não encontrado"
fi
echo ""

# Teste 3: Testar metadados do Brave
echo "3️⃣ Metadados do Brave:"
BRAVE_PLAYER=$(playerctl -l | grep -i brave | head -1)
if [ -n "$BRAVE_PLAYER" ]; then
    echo "   Player: $BRAVE_PLAYER"
    echo "   Status: $(playerctl -p "$BRAVE_PLAYER" status)"
    echo "   Título: $(playerctl -p "$BRAVE_PLAYER" metadata title)"
    echo "   Artista: $(playerctl -p "$BRAVE_PLAYER" metadata artist)"
else
    echo "   ❌ Nenhum player Brave encontrado"
fi
echo ""

# Teste 4: Testar script Python
echo "4️⃣ Testando script Python:"
if [ -f "modules/youtube_music.py" ]; then
    python3 modules/youtube_music.py
else
    echo "   ❌ Script não encontrado"
fi
echo ""

# Teste 5: Verificar se o módulo está configurado
echo "5️⃣ Verificando configuração da Waybar:"
if grep -q "custom/youtube-music" config.jsonc; then
    echo "   ✅ Módulo configurado na Waybar"
else
    echo "   ❌ Módulo não encontrado na configuração"
fi

echo ""
echo "🎯 Para testar:"
echo "   1. Abra o Brave"
echo "   2. Vá para music.youtube.com"
echo "   3. Toque uma música"
echo "   4. Recarregue a Waybar: pkill waybar && waybar &" 