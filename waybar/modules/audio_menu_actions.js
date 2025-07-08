// Script para ações do menu de áudio
// Este arquivo será usado pelo menu dropdown

function change_volume(delta) {
    // Muda o volume usando pactl
    const command = `pactl set-sink-volume @DEFAULT_SINK@ ${delta > 0 ? '+' : ''}${delta}%`;
    executeCommand(command);
    updateMenu();
}

function toggle_mute() {
    // Alterna o mute
    const command = 'pactl set-sink-mute @DEFAULT_SINK@ toggle';
    executeCommand(command);
    updateMenu();
}

function playerctl_play_pause() {
    // Play/pause da música
    const command = 'playerctl play-pause';
    executeCommand(command);
    updateMenu();
}

function playerctl_next() {
    // Próxima música
    const command = 'playerctl next';
    executeCommand(command);
    updateMenu();
}

function playerctl_previous() {
    // Música anterior
    const command = 'playerctl previous';
    executeCommand(command);
    updateMenu();
}

function set_device(device_id) {
    // Define dispositivo de áudio
    const command = `pactl set-default-sink ${device_id}`;
    executeCommand(command);
    updateMenu();
}

function open_pavucontrol() {
    // Abre o pavucontrol
    const command = 'pavucontrol';
    executeCommand(command);
}

function open_alsamixer() {
    // Abre o alsamixer no terminal
    const command = 'kitty --hold alsamixer';
    executeCommand(command);
}

function executeCommand(command) {
    // Executa comando via subprocess
    // Esta função seria chamada pelo Waybar
    console.log(`Executing: ${command}`);
    // Em uma implementação real, isso seria integrado com o Waybar
}

function updateMenu() {
    // Atualiza o menu após uma ação
    // Esta função seria chamada para recarregar o menu
    console.log('Updating menu...');
    // Em uma implementação real, isso recarregaria o menu
}

// Funções auxiliares para o menu
function showMenu() {
    // Mostra o menu dropdown
    const menu = document.getElementById('audio-menu');
    if (menu) {
        menu.style.display = 'block';
    }
}

function hideMenu() {
    // Esconde o menu dropdown
    const menu = document.getElementById('audio-menu');
    if (menu) {
        menu.style.display = 'none';
    }
}

// Event listeners para o menu
document.addEventListener('DOMContentLoaded', function() {
    // Adiciona event listeners quando o documento carrega
    const audioIcon = document.querySelector('.audio-menu-trigger');
    const menu = document.getElementById('audio-menu');
    
    if (audioIcon && menu) {
        // Mostra menu no hover
        audioIcon.addEventListener('mouseenter', showMenu);
        
        // Esconde menu quando mouse sai
        audioIcon.addEventListener('mouseleave', function(e) {
            // Verifica se o mouse não está sobre o menu
            if (!menu.contains(e.relatedTarget)) {
                hideMenu();
            }
        });
        
        // Mantém menu aberto quando mouse está sobre ele
        menu.addEventListener('mouseenter', function() {
            menu.style.display = 'block';
        });
        
        // Esconde menu quando mouse sai do menu
        menu.addEventListener('mouseleave', hideMenu);
    }
}); 