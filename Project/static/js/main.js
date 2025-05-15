// Mobile Menu Toggle
const sidebar = document.querySelector('.sidebar');
const menuToggle = document.createElement('button');
menuToggle.className = 'btn btn-primary d-md-none mobile-menu-toggle';
menuToggle.innerHTML = '<i class="fas fa-bars"></i>';
document.body.prepend(menuToggle);

menuToggle.addEventListener('click', () => {
    sidebar.classList.toggle('mobile-active');
});

// Card hover effect
document.querySelectorAll('.card-hover').forEach(card => {
    card.addEventListener('mousemove', (e) => {
        if (window.innerWidth > 768) {
            const xAxis = (window.innerWidth / 2 - e.pageX) / 25;
            const yAxis = (window.innerHeight / 2 - e.pageY) / 25;
            card.style.transform = `rotateY(${xAxis}deg) rotateX(${yAxis}deg)`;
        }
    });

    card.addEventListener('mouseleave', () => {
        card.style.transform = 'rotateY(0) rotateX(0)';
    });
});

// Smooth scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Form Validation
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', (e) => {
        const inputs = form.querySelectorAll('input, textarea');
        let isValid = true;

        inputs.forEach(input => {
            if (!input.checkValidity()) {
                isValid = false;
                input.classList.add('is-invalid');
            }
        });

        if (!isValid) {
            e.preventDefault();
            e.stopPropagation();
        }
    });
});

// Dynamic Year Update
document.getElementById('year').textContent = new Date().getFullYear();

// Image Lazy Loading
document.addEventListener("DOMContentLoaded", function() {
    const lazyImages = document.querySelectorAll('img.lazy');
    
    const lazyLoad = (target) => {
        const io = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    observer.unobserve(img);
                }
            });
        });

        io.observe(target);
    };

    lazyImages.forEach(lazyLoad);
});