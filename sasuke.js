// Loading screen functionality
window.addEventListener('load', function() {
    setTimeout(function() {
        const loading = document.getElementById('loading');
        loading.style.opacity = '0';
        setTimeout(function() {
            loading.style.display = 'none';
            animateHeroElements();
        }, 1000);
    }, 1500);
});

// Hero elements animation
function animateHeroElements() {
    const sasukeTitle = document.querySelector('.sasuke-title');
    const uchihaText = document.querySelector('.uchiha-text');
    const jutsuNav = document.querySelector('.jutsu-nav');
    const sasukeCircle = document.querySelector('.sasuke-circle');
    const heroText = document.querySelector('.hero-text');
    
    sasukeTitle.style.opacity = '0';
    uchihaText.style.opacity = '0';
    jutsuNav.style.opacity = '0';
    sasukeCircle.style.opacity = '0';
    heroText.style.opacity = '0';
    
    sasukeTitle.style.transform = 'translateY(50px)';
    uchihaText.style.transform = 'translateY(50px)';
    jutsuNav.style.transform = 'translateY(50px)';
    sasukeCircle.style.transform = 'translateX(50px)';
    heroText.style.transform = 'translateX(-50px)';
    
    sasukeTitle.style.transition = 'opacity 1s, transform 1s';
    uchihaText.style.transition = 'opacity 1s 0.2s, transform 1s 0.2s';
    jutsuNav.style.transition = 'opacity 1s 0.4s, transform 1s 0.4s';
    sasukeCircle.style.transition = 'opacity 1s 0.6s, transform 1s 0.6s';
    heroText.style.transition = 'opacity 1s 0.8s, transform 1s 0.8s';
    
    setTimeout(() => {
        sasukeTitle.style.opacity = '1';
        uchihaText.style.opacity = '1';
        jutsuNav.style.opacity = '1';
        sasukeCircle.style.opacity = '1';
        heroText.style.opacity = '1';
        
        sasukeTitle.style.transform = 'translateY(0)';
        uchihaText.style.transform = 'translateY(0)';
        jutsuNav.style.transform = 'translateY(0)';
        sasukeCircle.style.transform = 'translateX(0)';
        heroText.style.transform = 'translateX(0)';
    }, 100);
}

// Jutsu navigation functionality
document.addEventListener('DOMContentLoaded', function() {
    const jutsuItems = document.querySelectorAll('.jutsu-item');
    const sasukeImage = document.querySelector('.sasuke-image');
    
    jutsuItems[0].classList.add('active');
    
    const jutsuImages = {
        'Sharingan': 'images/sasuke-sharingan.png',
        'Chidori': 'images/sasuke-chidori.png',
        'Amaterasu': 'images/sasuke-amaterasu.png',
        'Susanoo': 'images/sasuke-susanoo.png'
    };
    
    jutsuItems.forEach(item => {
        item.addEventListener('click', function() {
            jutsuItems.forEach(i => i.classList.remove('active'));
            this.classList.add('active');
            
            const jutsuName = this.textContent;
            if (jutsuImages[jutsuName]) {
                sasukeImage.style.opacity = '0';
                setTimeout(() => {
                    sasukeImage.src = jutsuImages[jutsuName];
                    sasukeImage.style.opacity = '1';
                }, 300);
            }
        });
    });
    
    // Parallax effect
    document.addEventListener('mousemove', function(e) {
        const leftBg = document.querySelector('.left-bg');
        const rightBg = document.querySelector('.right-bg');
        
        const x = e.clientX / window.innerWidth;
        const y = e.clientY / window.innerHeight;
        
        leftBg.style.transform = `translateX(${x * 20}px) translateY(${y * 20}px)`;
        rightBg.style.transform = `translateX(${-x * 20}px) translateY(${-y * 20}px)`;
    });
});

// Drag to navigate back to Naruto page
const scrollIcon = document.querySelector('.scroll-icon');
let startX, startY, distX, distY;
const threshold = 100;
const restraint = 100;

scrollIcon.addEventListener('mousedown', function(e) {
    startX = e.pageX;
    startY = e.pageY;
    distX = 0;
    distY = 0;
    this.classList.add('dragging');
    e.preventDefault();
});

scrollIcon.addEventListener('mousemove', function(e) {
    if (!startX) return;
    distX = e.pageX - startX;
    distY = e.pageY - startY;
    e.preventDefault();
});

scrollIcon.addEventListener('mouseup', function(e) {
    if (!startX) return;
    
    if (Math.abs(distX) > threshold && Math.abs(distY) < restraint) {
        if (distX > 0) {
            window.location.href = this.dataset.narutoUrl;
        }
    }
    
    startX = null;
    startY = null;
    this.classList.remove('dragging');
    e.preventDefault();
});

// Touch events
scrollIcon.addEventListener('touchstart', function(e) {
    const touch = e.changedTouches[0];
    startX = touch.pageX;
    startY = touch.pageY;
    distX = 0;
    distY = 0;
    this.classList.add('dragging');
    e.preventDefault();
});

scrollIcon.addEventListener('touchmove', function(e) {
    if (!startX) return;
    const touch = e.changedTouches[0];
    distX = touch.pageX - startX;
    distY = touch.pageY - startY;
    e.preventDefault();
});

scrollIcon.addEventListener('touchend', function(e) {
    if (!startX) return;
    
    if (Math.abs(distX) > threshold && Math.abs(distY) < restraint) {
        if (distX > 0) {
            window.location.href = this.dataset.narutoUrl;
        }
    }
    
    startX = null;
    startY = null;
    this.classList.remove('dragging');
    e.preventDefault();
});