// Loading screen functionality
function initLoadingScreen() {
    window.addEventListener('load', function() {
        setTimeout(function() {
            const loading = document.getElementById('loading');
            if (!loading) return;
            
            loading.style.opacity = '0';
            setTimeout(function() {
                loading.style.display = 'none';
                animateHeroElements();
            }, 1000);
        }, 1500);
    });
}

// Hero elements animation
function animateHeroElements() {
    const narutoTitle = document.querySelector('.naruto-title');
    const uzumakiText = document.querySelector('.uzumaki-text');
    const jutsuNav = document.querySelector('.jutsu-nav');
    const narutoCircle = document.querySelector('.naruto-circle');
    const heroText = document.querySelector('.hero-text');
    
    // Set initial state
    narutoTitle.style.opacity = '0';
    uzumakiText.style.opacity = '0';
    jutsuNav.style.opacity = '0';
    narutoCircle.style.opacity = '0';
    heroText.style.opacity = '0';
    
    // Starting positions (drop down effect)
    narutoTitle.style.transform = 'translateY(50px)';
    uzumakiText.style.transform = 'translateY(50px)';
    jutsuNav.style.transform = 'translateY(50px)';
    narutoCircle.style.transform = 'translateX(50px)';
    heroText.style.transform = 'translateX(-50px)';
    
    // Set transitions with delays (same as Sasuke's)
    narutoTitle.style.transition = 'opacity 1s, transform 1s';
    uzumakiText.style.transition = 'opacity 1s 0.2s, transform 1s 0.2s';
    jutsuNav.style.transition = 'opacity 1s 0.4s, transform 1s 0.4s';
    narutoCircle.style.transition = 'opacity 1s 0.6s, transform 1s 0.6s';
    heroText.style.transition = 'opacity 1s 0.8s, transform 1s 0.8s';
    
    // Trigger animations
    setTimeout(() => {
        narutoTitle.style.opacity = '1';
        uzumakiText.style.opacity = '1';
        jutsuNav.style.opacity = '1';
        narutoCircle.style.opacity = '1';
        heroText.style.opacity = '1';
        
        narutoTitle.style.transform = 'translateY(0)';
        uzumakiText.style.transform = 'translateY(0)';
        jutsuNav.style.transform = 'translateY(0)';
        narutoCircle.style.transform = 'translateX(0)';
        heroText.style.transform = 'translateX(0)';
    }, 100);
}

// Jutsu navigation functionality
function initJutsuNavigation() {
    const jutsuItems = document.querySelectorAll('.jutsu-item');
    const narutoImage = document.querySelector('.naruto-image');
    
    if (!jutsuItems.length || !narutoImage) return;

    const jutsuImages = {
        'Sage Mode': 'images/Naruto_with_coat 1.png',
        'Rasen-Shuriken': 'images/Rasen-Shuriken.png',
        'Frog-Kumite': 'images/naruto-frog-kumite.png',
        'Kurama-Chakra': 'images/naruto-kurama-mode.png'
    };

    // Set initial active state
    jutsuItems[0]?.classList.add('active');

    // Add click event listeners
    jutsuItems.forEach(item => {
        item.addEventListener('click', function() {
            // Update active state
            jutsuItems.forEach(i => i.classList.remove('active'));
            this.classList.add('active');
            
            // Update image
            const jutsuName = this.textContent;
            if (jutsuImages[jutsuName]) {
                narutoImage.style.opacity = '0';
                setTimeout(() => {
                    narutoImage.src = jutsuImages[jutsuName];
                    narutoImage.style.opacity = '1';
                }, 300);
            }
        });
    });
}

// Parallax effect
function initParallax() {
    const leftBg = document.querySelector('.left-bg');
    const rightBg = document.querySelector('.right-bg');
    
    if (!leftBg || !rightBg) return;

    document.addEventListener('mousemove', function(e) {
        const x = e.clientX / window.innerWidth;
        const y = e.clientY / window.innerHeight;
        
        leftBg.style.transform = `translateX(${x * 20}px) translateY(${y * 20}px)`;
        rightBg.style.transform = `translateX(${-x * 20}px) translateY(${-y * 20}px)`;
    });
}

// Drag to navigate functionality - Fixed Version
function initDragNavigation() {
    const scrollIcon = document.querySelector('.scroll-icon');
    if (!scrollIcon) return;

    let startX = null;
    let startY = null;
    let isDragging = false;
    const threshold = 100; // Minimum horizontal drag distance required
    const maxVerticalDrift = 50; // Maximum allowed vertical movement during drag

    // Mouse event handlers
    function handleDragStart(e) {
        isDragging = true;
        startX = e.clientX || e.touches[0].clientX;
        startY = e.clientY || e.touches[0].clientY;
        scrollIcon.classList.add('dragging');
        e.preventDefault();
    }

    function handleDragMove(e) {
        if (!isDragging) return;
        e.preventDefault();
    }

    function handleDragEnd(e) {
        if (!isDragging) return;
        
        const endX = e.clientX || (e.changedTouches && e.changedTouches[0].clientX);
        const endY = e.clientY || (e.changedTouches && e.changedTouches[0].clientY);
        
        if (!endX || !endY || startX === null || startY === null) {
            resetDragState();
            return;
        }

        const distX = endX - startX;
        const distY = endY - startY;

        // Check if horizontal drag exceeds threshold and vertical drift is within limits
        if (distX > threshold && Math.abs(distY) < maxVerticalDrift) {
            // Navigate to Sasuke page
            window.location.href = scrollIcon.dataset.sasukeUrl || 'sasuke.html';
        }

        resetDragState();
        e.preventDefault();
    }

    function resetDragState() {
        isDragging = false;
        startX = null;
        startY = null;
        scrollIcon.classList.remove('dragging');
    }

    // Add event listeners
    scrollIcon.addEventListener('mousedown', handleDragStart);
    document.addEventListener('mousemove', handleDragMove);
    document.addEventListener('mouseup', handleDragEnd);
    
    scrollIcon.addEventListener('touchstart', handleDragStart, { passive: false });
    document.addEventListener('touchmove', handleDragMove, { passive: false });
    document.addEventListener('touchend', handleDragEnd);
}

// Initialize all functionality
document.addEventListener('DOMContentLoaded', function() {
    initLoadingScreen();
    initJutsuNavigation();
    initParallax();
    initDragNavigation(); // Make sure this is called
});