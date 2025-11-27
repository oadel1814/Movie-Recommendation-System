// Search functionality
const searchInput = document.getElementById('searchInput');
const searchResults = document.getElementById('searchResults');
let searchTimeout;

if (searchInput) {
    searchInput.addEventListener('input', function(e) {
        const query = e.target.value.trim();
        
        clearTimeout(searchTimeout);
        
        if (query.length < 2) {
            searchResults.classList.remove('active');
            return;
        }
        
        searchTimeout = setTimeout(() => {
            fetch(`/search?q=${encodeURIComponent(query)}`)
                .then(res => res.json())
                .then(data => {
                    displaySearchResults(data);
                })
                .catch(err => console.error('Search error:', err));
        }, 300);
    });
    
    // Close search results when clicking outside
    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
            searchResults.classList.remove('active');
        }
    });
}

function displaySearchResults(results) {
    if (results.length === 0) {
        searchResults.innerHTML = '<div style="padding: 15px; color: #888;">No results found</div>';
        searchResults.classList.add('active');
        return;
    }
    
    const html = results.map(movie => `
        <a href="/movie/${movie.id}" class="search-result-item" style="display: flex; align-items: center; gap: 10px; text-decoration: none; color: inherit;">
            <img src="${movie.poster ? 'https://image.tmdb.org/t/p/w500' + movie.poster : 'https://via.placeholder.com/40x60?text=?'}" 
                 alt="${movie.title}" 
                 style="width: 40px; height: 60px; object-fit: cover; border-radius: 3px;">
            <div>
                <div style="font-weight: 500;">${movie.title}</div>
                <div style="font-size: 0.85em; color: #888;">
                    ${movie.year} • ⭐ ${movie.rating}
                </div>
            </div>
        </a>
    `).join('');
    
    searchResults.innerHTML = html;
    searchResults.classList.add('active');
}

// Alert auto-dismiss
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.animation = 'slideUp 0.3s ease';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
});

// Slide up animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideUp {
        to {
            opacity: 0;
            transform: translateY(-20px);
        }
    }
`;
document.head.appendChild(style);