// Functionality for the Nova IA section
document.addEventListener('DOMContentLoaded', function() {
    const addCategoriaBtn = document.getElementById('add-categoria-btn');
    const categoriasContainer = document.querySelector('.categorias-container');
    const categoriaInfo = document.querySelector('.categoria-info');
    
    if (addCategoriaBtn) {
        addCategoriaBtn.addEventListener('click', function() {
            const categoriaItems = document.querySelectorAll('.categoria-item');
            
            if (categoriaItems.length < 5) {
                const newItem = document.createElement('div');
                newItem.className = 'categoria-item';
                newItem.innerHTML = `
                    <input type="text" name="categoria-${categoriaItems.length + 1}" 
                           placeholder="Categoria ${categoriaItems.length + 1}" class="categoria-input">
                    <button type="button" class="remove-categoria-btn">-</button>
                `;
                
                categoriasContainer.appendChild(newItem);
                
                // Enable the first remove button if it was disabled
                if (categoriaItems.length === 1) {
                    document.querySelector('.remove-categoria-btn').disabled = false;
                }
                
                // Update counter
                updateCategoriaCounter();
                
                // Add event listener to new remove button
                const removeBtn = newItem.querySelector('.remove-categoria-btn');
                removeBtn.addEventListener('click', function() {
                    categoriasContainer.removeChild(newItem);
                    updateCategoriaCounter();
                    
                    // If only one category remains, disable its remove button
                    const remainingItems = document.querySelectorAll('.categoria-item');
                    if (remainingItems.length === 1) {
                        remainingItems[0].querySelector('.remove-categoria-btn').disabled = true;
                    }
                    
                    // Rename remaining categories for proper sequence
                    renameCategories();
                });
            }
            
            // Disable add button if max reached
            if (document.querySelectorAll('.categoria-item').length >= 5) {
                addCategoriaBtn.disabled = true;
            }
        });
    }
    
    function updateCategoriaCounter() {
        const count = document.querySelectorAll('.categoria-item').length;
        categoriaInfo.textContent = `${count} de 5 categorias adicionadas`;
        
        // Re-enable add button if below max
        if (count < 5) {
            addCategoriaBtn.disabled = false;
        }
    }
    
    function renameCategories() {
        const items = document.querySelectorAll('.categoria-item');
        items.forEach((item, index) => {
            const input = item.querySelector('input');
            input.name = `categoria-${index + 1}`;
            input.placeholder = `Categoria ${index + 1}`;
        });
    }
});