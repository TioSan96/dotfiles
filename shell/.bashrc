#
# ~/.bashrc
#
# Mostra imagem no terminal com fastfetch e kitty graphics
FASTFETCH_IMAGE="$HOME/Imagens/kisame.png"
if command -v fastfetch >/dev/null 2>&1; then
  fastfetch --kitty-direct "$FASTFETCH_IMAGE"
fi
# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'
alias grep='grep --color=auto'
PS1='[\u@\h \W]\$ '


# Created by `pipx` on 2025-07-05 21:44:33
export PATH="$PATH:/home/hotplugin/.local/bin"
export PATH="$HOME/.local/bin:$PATH"
