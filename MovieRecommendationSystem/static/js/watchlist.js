// Toggle watchlist
async function toggleWatchlist(movieId, button) {
    const isInWatchlist = button.classList.contains('in-watchlist');
    const endpoint = isInWatchlist ? '/watchlist/remove' : '/watchlist/add';
    
    const originalText = button.textContent;
    button.textContent = '...';
    button.disabled = true;
    
    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ movie_id: movieId })
        });
        
        const data = await response.json();
        
        if (data.success) {
            if (isInWatchlist) {
                button.classList.remove('in-watchlist');
                button.textContent = '+ Watchlist';
            } else {
                button.classList.add('in-watchlist');
                button.textContent = '✓ In Watchlist';
            }
            showToast(data.message, 'success');
        } else {
            button.textContent = originalText;
            showToast(data.message, 'error');
        }
    } catch (error) {
        button.textContent = originalText;
        showToast('An error occurred', 'error');
        console.error('Error:', error);
    } finally {
        button.disabled = false;
    }
}

// Remove from watchlist (on watchlist page)
async function removeFromWatchlist(movieId, button) {
    if (!confirm('Remove this movie from your watchlist?')) {
        return;
    }
    
    button.textContent = '...';
    button.disabled = true;
    
    try {
        const response = await fetch('/watchlist/remove', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ movie_id: movieId })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Remove the movie card with animation
            const movieCard = button.closest('.movie-card');
            movieCard.style.animation = 'fadeOut 0.3s ease';
            setTimeout(() => {
                movieCard.remove();
                
                // Check if watchlist is empty
                const grid = document.querySelector('.movies-grid');
                if (grid && grid.children.length === 0) {
                    location.reload();
                }
            }, 300);
            
            showToast(data.message, 'success');
        } else {
            button.textContent = 'Remove';
            button.disabled = false;
            showToast(data.message, 'error');
        }
    } catch (error) {
        button.textContent = 'Remove';
        button.disabled = false;
        showToast('An error occurred', 'error');
        console.error('Error:', error);
    }
}

// Toggle watched status
async function toggleWatched(movieId, button) {
    const originalText = button.textContent;
    button.textContent = '...';
    button.disabled = true;
    
    try {
        const response = await fetch('/watchlist/toggle-watched', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ movie_id: movieId })
        });
        
        const data = await response.json();
        
        if (data.success) {
            if (data.watched) {
                button.classList.add('watched');
                button.textContent = '✓ Watched';
            } else {
                button.classList.remove('watched');
                button.textContent = 'Mark as Watched';
            }
            showToast(data.watched ? 'Marked as watched' : 'Unmarked', 'success');
        } else {
            button.textContent = originalText;
            showToast(data.message, 'error');
        }
    } catch (error) {
        button.textContent = originalText;
        showToast('An error occurred', 'error');
        console.error('Error:', error);
    } finally {
        button.disabled = false;
    }
}

// Toast notification
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        padding: 15px 25px;
        background: ${type === 'success' ? '#1e5128' : type === 'error' ? '#5a1a1a' : '#1a3a5a'};
        color: white;
        border-radius: 5px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
        z-index: 1000;
        animation: slideInRight 0.3s ease;
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Check watchlist status on page load
document.addEventListener('DOMContentLoaded', async function() {
    const watchlistButtons = document.querySelectorAll('.btn-watchlist[data-movie-id]');
    
    for (const button of watchlistButtons) {
        const movieId = button.dataset.movieId;
        
        try {
            const response = await fetch(`/check-watchlist/${movieId}`);
            const data = await response.json();
            
            if (data.in_watchlist) {
                button.classList.add('in-watchlist');
                button.textContent = '✓ In Watchlist';
            }
        } catch (error) {
            console.error('Error checking watchlist:', error);
        }
    }
});

// Add animations
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeOut {
        to {
            opacity: 0;
            transform: scale(0.9);
        }
    }
    
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);