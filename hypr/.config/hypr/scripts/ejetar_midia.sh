#!/bin/bash

# Listar os dispositivos removíveis com lsblk e filtrar apenas os que têm partições montadas
# Ajuste os filtros conforme necessário para identificar corretamente suas mídias removíveis

DISPOSITIVOS=$(lsblk -o NAME,SIZE,MOUNTPOINT,TYPE | grep -E 'disk|part' | grep -v loop | grep -v sr0)

# Verifique se há dispositivos removíveis disponíveis
if [ -z "$DISPOSITIVOS" ]; then
  echo "Nenhuma mídia removível encontrada."
  exit 1
fi

# Exibir os dispositivos removíveis e permitir a seleção interativa com fzf
DISPOSITIVO_SELECIONADO=$(echo "$DISPOSITIVOS" | fzf --prompt="Selecione uma mídia para ejetar: ")

# Verifique se a seleção não está vazia
if [ -z "$DISPOSITIVO_SELECIONADO" ]; then
  echo "Nenhuma mídia selecionada."
  exit 1
fi

# Extrair o dispositivo selecionado (ex: sdb, sdc)
DISPOSITIVO=$(echo "$DISPOSITIVO_SELECIONADO" | awk '{print $1}')

# Ejetar o dispositivo selecionado
udisksctl power-off -b /dev/$DISPOSITIVO

# Mensagem de confirmação
echo "Mídia /dev/$DISPOSITIVO ejetada com sucesso."

