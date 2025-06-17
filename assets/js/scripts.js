// Função para mostrar a seção clicada
function showSection(sectionId) {
    // Esconde todas as seções
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => {
        section.classList.remove('active');
    });

    // Mostra a seção correspondente
    const section = document.getElementById(sectionId);
    section.classList.add('active');
}



// Mostrar a primeira seção por padrão
document.addEventListener('DOMContentLoaded', () => {
    showSection('perfil');
});
