// Navbar scroll effect
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 50);
});

// Mobile nav toggle
const navToggle = document.getElementById('navToggle');
const navLinks  = document.getElementById('navLinks');
if (navToggle) {
    navToggle.addEventListener('click', () => {
        navLinks.classList.toggle('open');
        document.body.style.overflow = navLinks.classList.contains('open') ? 'hidden' : '';
    });
    navLinks.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('open');
            document.body.style.overflow = '';
        });
    });
    document.addEventListener('click', (e) => {
        if (!navbar.contains(e.target) && navLinks.classList.contains('open')) {
            navLinks.classList.remove('open');
            document.body.style.overflow = '';
        }
    });
}

// Animate elements on scroll
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

document.querySelectorAll('.service-card, .room-card, .testimonial-card, .value-card, .team-card, .award-item, .gallery-item').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(24px)';
    el.style.transition = 'opacity 0.55s ease, transform 0.55s ease';
    observer.observe(el);
});

// Set min check-in date to today
const checkin  = document.getElementById('checkin');
const checkout = document.getElementById('checkout');
if (checkin) {
    const today = new Date().toISOString().split('T')[0];
    checkin.min = today;
    checkin.value = today;
    checkin.addEventListener('change', () => {
        if (checkout) {
            checkout.min = checkin.value;
            if (checkout.value && checkout.value <= checkin.value) {
                const next = new Date(checkin.value);
                next.setDate(next.getDate() + 1);
                checkout.value = next.toISOString().split('T')[0];
            }
        }
    });
    if (checkout) {
        const tomorrow = new Date();
        tomorrow.setDate(tomorrow.getDate() + 1);
        checkout.min = tomorrow.toISOString().split('T')[0];
        checkout.value = tomorrow.toISOString().split('T')[0];
    }
}
