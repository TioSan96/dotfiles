#!/usr/bin/env bash

# Arquivos temporários
updates_file="/tmp/waybar-updates"
list_file="/tmp/waybar-updates-list"
notified_updates_file="/tmp/waybar-notified-updates"

# Função para verificar pacotes do sistema com checkupdates
verificar_repositorios() {
    checkupdates 2>/dev/null
}

# Função para verificar pacotes do AUR com yay
verificar_aur() {
    yay -Qu --aur 2>/dev/null
}

# Função para verificar atualizações do Flatpak
verificar_flatpak() {
    flatpak remote-ls --updates 2>/dev/null | awk '{print $1 " -> " $3}'
}

# Função para formatar strings para o tooltip
string_to_len() {
    local string="$1"
    local len="$2"
    if [ ${#string} -gt "$len" ]; then
        echo "${string:0:$((len - 2))}.."
    else
        printf "%-20s" "$string"
    fi
}

# Verifica pacotes para atualização
repositorios=$(verificar_repositorios)
aur=$(verificar_aur)
flatpaks=$(verificar_flatpak)

# Combina todas as atualizações
if [ -n "$repositorios" ] || [ -n "$aur" ] || [ -n "$flatpaks" ]; then
    # Contagem total de atualizações
    total_updates=$(($(echo "$repositorios" | grep -c '^') + $(echo "$aur" | grep -c '^') + $(echo "$flatpaks" | grep -c '^')))
    echo "$total_updates" > "$updates_file"
    echo -e "$repositorios\n$aur\n$flatpaks" > "$list_file"

    # Construção do tooltip detalhado
    tooltip="<b>$total_updates atualizações disponíveis</b>\n"
    tooltip+="<b>$(string_to_len "Pacote" 20) $(string_to_len "Versão Atual" 20) $(string_to_len "Nova Versão" 20)</b>\n"

    formatar_atualizacoes() {
        local updates="$1"
        while IFS= read -r line; do
            local pacote versao_antiga versao_nova
            pacote=$(string_to_len "$(echo "$line" | awk '{print $1}')" 20)
            versao_antiga=$(string_to_len "$(echo "$line" | awk '{print $2}')" 20)
            versao_nova=$(string_to_len "$(echo "$line" | awk '{print $4}')" 20)
            tooltip+="<b>$pacote</b> $versao_antiga $versao_nova\n"
        done <<< "$updates"
    }

    formatar_atualizacoes "$repositorios"
    formatar_atualizacoes "$aur"

    while IFS= read -r line; do
        local pacote
        pacote=$(string_to_len "$(echo "$line" | awk '{print $1}')" 20)
        tooltip+="<b>$pacote</b>\n"
    done <<< "$flatpaks"

    tooltip=${tooltip::-2} # Remove a última quebra de linha

    # Verifica atualizações novas
    new_updates=$(echo -e "$repositorios\n$aur\n$flatpaks")
    if [ ! -f "$notified_updates_file" ]; then
        touch "$notified_updates_file"
    fi
    new_to_notify=$(comm -23 <(echo "$new_updates" | sort) <(sort "$notified_updates_file"))

    # Se houver novas atualizações, notifica e atualiza o histórico
    if [ -n "$new_to_notify" ]; then
        notify-send -u low -t 5000 "Novas atualizações disponíveis" \
            "Há $(echo "$new_to_notify" | wc -l) novas atualizações pendentes:\n$(echo -e "$new_to_notify" | sed 's/<[^>]*>//g')"
        echo "$new_updates" > "$notified_updates_file"
    fi

    # Exibe no Waybar
    cat <<EOF
{ "text": "$total_updates", "tooltip": "$tooltip" }
EOF
else
    echo "0" > "$updates_file"
    echo "" > "$list_file"

    # Exibe no Waybar
    cat <<EOF
{ "text": "", "tooltip": "<b>Sistema atualizado</b>" }
EOF
fi
