document.addEventListener('DOMContentLoaded', function() {
    // Adicionar CSS inline para criar nosso próprio estilo de checkbox
    const style = document.createElement('style');
    style.textContent = `
        .favorite-container {
            display: inline-flex;
            align-items: center;
            cursor: pointer;
        }
        
        .custom-checkbox {
            display: inline-block;
            width: 18px;
            height: 18px;
            border: 2px solid #aaa;
            border-radius: 3px;
            margin-right: 8px;
            position: relative;
            background-color: white;
            cursor: pointer;
        }
        
        .custom-checkbox.checked {
            background-color: #4a90e2;
            border-color: #4a90e2;
        }
        
        .custom-checkbox.checked:after {
            content: '✓';
            position: absolute;
            color: white;
            font-size: 14px;
            top: -1px;
            left: 3px;
        }
        
        .favorite-checkbox {
            display: none; /* Escondemos o checkbox original */
        }
    `;
    document.head.appendChild(style);

    // Initialize favorite items from localStorage if available
    const favorites = JSON.parse(localStorage.getItem('aiToolsFavorites')) || [];
    
    // Função para transformar todos os checkboxes em custom checkboxes
    function setupCustomCheckboxes() {
        // Encontrar todos os checkboxes originais
        document.querySelectorAll('.favorite-checkbox').forEach(checkbox => {
            // Verificar se já foi processado
            if (checkbox.hasAttribute('data-processed')) return;
            
            // Marcar como processado para evitar duplicação
            checkbox.setAttribute('data-processed', 'true');
            
            // Criar o elemento visual customizado
            const customCheckbox = document.createElement('span');
            customCheckbox.className = 'custom-checkbox';
            
            // Verificar se deve começar marcado
            const card = checkbox.closest('.card');
            const cardName = card ? card.getAttribute('data-name') : null;
            
            if (cardName && favorites.some(fav => fav.name === cardName)) {
                customCheckbox.classList.add('checked');
                checkbox.checked = true;
            }
            
            // Inserir o elemento customizado antes da label
            const container = checkbox.closest('.favorite-container');
            container.insertBefore(customCheckbox, checkbox.nextSibling);
            
            // Adicionar evento de clique no elemento customizado
            customCheckbox.addEventListener('click', function(e) {
                e.stopPropagation();
                
                // Alternar a classe visual imediatamente
                this.classList.toggle('checked');
                
                // Atualizar o checkbox oculto
                checkbox.checked = this.classList.contains('checked');
                
                // Processar favoritos
                const card = checkbox.closest('.card');
                const name = card.getAttribute('data-name');
                const url = card.getAttribute('data-url');
                const category = card.getAttribute('data-category');
                
                // Get current favorites
                let favorites = JSON.parse(localStorage.getItem('aiToolsFavorites')) || [];
                
                if (checkbox.checked) {
                    // Add to favorites if not already there
                    if (!favorites.some(fav => fav.name === name)) {
                        favorites.push({
                            name,
                            url,
                            category,
                            cardHtml: card.outerHTML
                        });
                    }
                } else {
                    // Remove from favorites
                    favorites = favorites.filter(fav => fav.name !== name);
                }
                
                // Save back to localStorage
                localStorage.setItem('aiToolsFavorites', JSON.stringify(favorites));
                
                // Sincronizar outros checkboxes
                document.querySelectorAll(`.card[data-name="${name}"] .custom-checkbox`).forEach(cb => {
                    if (cb !== this) {
                        if (checkbox.checked) {
                            cb.classList.add('checked');
                        } else {
                            cb.classList.remove('checked');
                        }
                    }
                });
                
                // Atualizar a seção de favoritos
                updateFavoritesFromStorage(favorites);
            });
        });
    }
    
    // Set up menu navigation
    const menuButtons = document.querySelectorAll('.menu button');
    const sections = document.querySelectorAll('.section');
    
    menuButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons and sections
            menuButtons.forEach(btn => btn.classList.remove('active'));
            sections.forEach(section => section.classList.remove('active'));
            
            // Add active class to clicked button
            this.classList.add('active');
            
            // Show corresponding section
            const sectionId = this.getAttribute('data-section');
            document.getElementById(sectionId).classList.add('active');
            
            // Configurar checkboxes customizados após mudar de seção
            setTimeout(setupCustomCheckboxes, 0);
        });
    });
    
    // Make cards clickable to open websites
    const cards = document.querySelectorAll('.card');
    
    cards.forEach(card => {
        card.addEventListener('click', function(e) {
            // Don't navigate if clicking on checkbox elements
            if (e.target.classList.contains('favorite-checkbox') || 
                e.target.classList.contains('favorite-label') ||
                e.target.classList.contains('custom-checkbox')) {
                return;
            }
            
            // Get the URL from the card's data attribute
            const url = this.getAttribute('data-url');
            if (url) {
                window.open(url, '_blank');
            }
        });
    });
    
    // Function to update favorites section
    function updateFavoritesFromStorage(favorites) {
        const favoritesGallery = document.getElementById('favoritos-gallery');
        const noFavoritesMessage = document.getElementById('no-favorites');
        
        // Clear and rebuild favorites section
        // Keep the "no favorites" message element
        while (favoritesGallery.children.length > 1) {
            favoritesGallery.removeChild(favoritesGallery.lastChild);
        }
        
        if (favorites.length > 0) {
            noFavoritesMessage.style.display = 'none';
            
            // Create cards for each favorite
            favorites.forEach(favorite => {
                // Create a new card
                const card = document.createElement('div');
                card.className = 'card';
                card.setAttribute('data-url', favorite.url);
                card.setAttribute('data-name', favorite.name);
                card.setAttribute('data-category', favorite.category);
                
                const cardHeader = document.createElement('div');
                cardHeader.className = 'card-header';
                
                const cardTitle = document.createElement('h3');
                cardTitle.textContent = favorite.name;
                
                cardHeader.appendChild(cardTitle);
                card.appendChild(cardHeader);
                
                const cardContent = document.createElement('div');
                cardContent.className = 'card-content';
                
                // Find original card to copy tags
                const originalCard = document.querySelector(`.card[data-name="${favorite.name}"]`);
                if (originalCard) {
                    const tagsContainer = originalCard.querySelector('.tags');
                    if (tagsContainer) {
                        cardContent.appendChild(tagsContainer.cloneNode(true));
                    }
                }
                
                const url = document.createElement('span');
                url.className = 'url';
                url.textContent = favorite.url.replace('https://', '');
                cardContent.appendChild(url);
                
                const favoriteContainer = document.createElement('label');
                favoriteContainer.className = 'favorite-container';
                
                const favoriteCheckbox = document.createElement('input');
                favoriteCheckbox.type = 'checkbox';
                favoriteCheckbox.className = 'favorite-checkbox';
                favoriteCheckbox.checked = true;
                
                const favoriteLabel = document.createElement('span');
                favoriteLabel.className = 'favorite-label';
                favoriteLabel.textContent = 'Remover dos Favoritos';
                
                favoriteContainer.appendChild(favoriteCheckbox);
                favoriteContainer.appendChild(favoriteLabel);
                cardContent.appendChild(favoriteContainer);
                
                card.appendChild(cardContent);
                
                // Add event listeners
                card.addEventListener('click', function(e) {
                    if (e.target.classList.contains('favorite-checkbox') || 
                        e.target.classList.contains('favorite-label') ||
                        e.target.classList.contains('custom-checkbox')) {
                        return;
                    }
                    window.open(favorite.url, '_blank');
                });
                
                favoritesGallery.appendChild(card);
            });
            
            // Configurar checkboxes customizados nos favoritos
            setTimeout(setupCustomCheckboxes, 0);
        } else {
            noFavoritesMessage.style.display = 'block';
        }
    }
    
    // Inicializar a interface
    updateFavoritesFromStorage(favorites);
    setupCustomCheckboxes();
});