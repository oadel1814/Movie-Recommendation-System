// Additional recommendation page functionality
document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scroll animation
    window.scrollTo({ top: 0, behavior: 'smooth' });
    
    // Animate movie cards on load
    const movieCards = document.querySelectorAll('.movie-card');
    movieCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 50);
    });
});

// Refresh recommendations
function refreshRecommendations() {
    const button = document.querySelector('.btn-refresh');
    if (button) {
        button.textContent = 'Refreshing...';
        button.disabled = true;
        location.reload();
    }
}