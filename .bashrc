#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

# system info on new shells (Kitty image via fastfetch)
fastfetch --kitty-direct /home/hotplugin/Transferências/kisame.png

alias ls='ls --color=auto'
alias grep='grep --color=auto'
PS1='[\u@\h \W]\$ '

# Created by `pipx` on 2025-07-05 21:44:33
export PATH="$PATH:/home/hotplugin/.local/bin"
