/**
 * E-GOVERNANCE PLATFORM - ANIMATION CONTROLLER
 * Professional UX Animations & Interactions
 * Government-Grade Premium Experience
 */

(function () {
    'use strict';

    // ========================================
    // ACCESSIBILITY CHECK
    // ========================================

    /**
     * Check if user prefers reduced motion
     */
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (prefersReducedMotion) {
        console.log('Reduced motion preference detected. Animations minimized.');
    }

    // ========================================
    // DOCUMENT READY INITIALIZATION
    // ========================================

    document.addEventListener('DOMContentLoaded', function () {

        // Initialize all animation features
        initScrollAnimations();
        initCardAnimations();
        initNavbarScroll();
        initCountUpAnimations();
        initSearchEnhancements();
        initFormValidationAnimations();
        initTooltips();

        console.log('✓ Theme animations initialized');
    });

    // ========================================
    // SCROLL-BASED ANIMATIONS
    // ========================================

    /**
     * Initialize Intersection Observer for scroll animations
     */
    function initScrollAnimations() {
        if (prefersReducedMotion) return;

        // Create observer for elements that should animate on scroll
        const observerOptions = {
            threshold: 0.15,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver(function (entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    // Optionally unobserve after animation
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        // Observe all elements with scroll animation classes
        const scrollElements = document.querySelectorAll('.scroll-fade, .scroll-left, .scroll-right');
        scrollElements.forEach(el => observer.observe(el));

        // Auto-add scroll animation to sections
        const sections = document.querySelectorAll('section, .container > .row, .info-section');
        sections.forEach((section, index) => {
            if (!section.classList.contains('scroll-fade')) {
                section.classList.add('scroll-fade');
                observer.observe(section);
            }
        });
    }

    // ========================================
    // CARD STAGGER ANIMATIONS
    // ========================================

    /**
     * Add staggered entrance animation to cards
     */
    function initCardAnimations() {
        if (prefersReducedMotion) return;

        // Find all card containers
        const cardContainers = document.querySelectorAll('.row, .card-group, .list-group');

        cardContainers.forEach(container => {
            const cards = container.querySelectorAll('.card');

            if (cards.length > 0) {
                const observer = new IntersectionObserver(function (entries) {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            const cards = entry.target.querySelectorAll('.card');
                            cards.forEach((card, index) => {
                                if (!card.classList.contains('card-animate')) {
                                    card.classList.add('card-animate');
                                    card.style.animationDelay = `${index * 60}ms`;
                                }
                            });
                            observer.unobserve(entry.target);
                        }
                    });
                }, { threshold: 0.1 });

                observer.observe(container);
            }
        });
    }

    // ========================================
    // NAVBAR SCROLL EFFECT
    // ========================================

    /**
     * Add background and shadow to navbar on scroll
     */
    function initNavbarScroll() {
        const navbar = document.querySelector('.navbar');
        if (!navbar) return;

        let lastScroll = 0;
        const scrollThreshold = 50;

        window.addEventListener('scroll', function () {
            const currentScroll = window.pageYOffset;

            if (currentScroll > scrollThreshold) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }

            lastScroll = currentScroll;
        }, { passive: true });
    }

    // ========================================
    // NUMBER COUNT-UP ANIMATION
    // ========================================

    /**
     * Animate numbers counting up for statistics
     */
    function initCountUpAnimations() {
        if (prefersReducedMotion) return;

        const statNumbers = document.querySelectorAll('.stat-number, .count-up, [data-count-up]');

        const observer = new IntersectionObserver(function (entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting && !entry.target.dataset.counted) {
                    animateNumber(entry.target);
                    entry.target.dataset.counted = 'true';
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        statNumbers.forEach(el => observer.observe(el));
    }

    /**
     * Count up animation for a number element
     */
    function animateNumber(element) {
        const target = parseInt(element.textContent.replace(/[^0-9]/g, '')) || 0;
        const duration = 1200; // milliseconds
        const increment = target / (duration / 16); // 60fps
        let current = 0;

        const timer = setInterval(function () {
            current += increment;
            if (current >= target) {
                element.textContent = formatNumber(target);
                clearInterval(timer);
            } else {
                element.textContent = formatNumber(Math.floor(current));
            }
        }, 16);
    }

    /**
     * Format number with commas
     */
    function formatNumber(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    }

    // ========================================
    // SEARCH BAR ENHANCEMENTS
    // ========================================

    /**
     * Enhanced search input interactions
     */
    function initSearchEnhancements() {
        const searchInputs = document.querySelectorAll('input[type="search"], .search-input');

        searchInputs.forEach(input => {
            // Add pill-shaped styling
            input.classList.add('rounded-pill');

            // Store original width
            const originalWidth = input.offsetWidth;

            input.addEventListener('focus', function () {
                this.style.borderColor = '#D97706';

                // Expand on desktop
                if (window.innerWidth >= 768) {
                    this.style.width = (originalWidth * 1.1) + 'px';
                }
            });

            input.addEventListener('blur', function () {
                this.style.borderColor = '';
                this.style.width = originalWidth + 'px';
            });

            // Real-time search highlighting (if results exist)
            input.addEventListener('input', function () {
                const query = this.value.toLowerCase();
                if (query.length > 0) {
                    highlightSearchResults(query);
                } else {
                    clearSearchHighlights();
                }
            });
        });
    }

    /**
     * Highlight matching text in search results
     */
    function highlightSearchResults(query) {
        const results = document.querySelectorAll('.search-result, .list-group-item, .card');

        results.forEach(result => {
            const text = result.textContent.toLowerCase();
            if (text.includes(query)) {
                result.style.display = '';
                // Add subtle gold background
                result.style.borderLeft = '3px solid #D97706';
            } else {
                // Optionally hide non-matching results
                // result.style.display = 'none';
            }
        });
    }

    /**
     * Clear search highlights
     */
    function clearSearchHighlights() {
        const results = document.querySelectorAll('.search-result, .list-group-item, .card');
        results.forEach(result => {
            result.style.display = '';
            result.style.borderLeft = '';
        });
    }

    // ========================================
    // FORM VALIDATION ANIMATIONS
    // ========================================

    /**
     * Enhanced form validation feedback
     */
    function initFormValidationAnimations() {
        const forms = document.querySelectorAll('form');

        forms.forEach(form => {
            const inputs = form.querySelectorAll('input, textarea, select');

            inputs.forEach(input => {
                input.addEventListener('invalid', function (e) {
                    e.preventDefault();
                    this.classList.add('is-invalid');

                    // Shake animation
                    if (!prefersReducedMotion) {
                        this.style.animation = 'none';
                        setTimeout(() => {
                            this.style.animation = 'inputShake 400ms ease';
                        }, 10);
                    }
                });

                input.addEventListener('input', function () {
                    if (this.checkValidity()) {
                        this.classList.remove('is-invalid');
                        this.classList.add('is-valid');
                    }
                });
            });
        });
    }

    // ========================================
    // TOOLTIP INITIALIZATION
    // ========================================

    /**
     * Initialize Bootstrap tooltips with custom animation
     */
    function initTooltips() {
        // Check if Bootstrap tooltip is available
        if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
            const tooltipTriggerList = [].slice.call(
                document.querySelectorAll('[data-bs-toggle="tooltip"]')
            );

            tooltipTriggerList.map(function (tooltipTriggerEl) {
                return new bootstrap.Tooltip(tooltipTriggerEl, {
                    animation: true,
                    delay: { show: 200, hide: 100 }
                });
            });
        }
    }

    // ========================================
    // BUTTON RIPPLE EFFECT
    // ========================================

    /**
     * Add ripple effect to buttons on click
     */
    document.addEventListener('click', function (e) {
        if (prefersReducedMotion) return;

        const button = e.target.closest('.btn');
        if (!button) return;

        // Create ripple element
        const ripple = document.createElement('span');
        const rect = button.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;

        ripple.style.cssText = `
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.6);
            width: ${size}px;
            height: ${size}px;
            left: ${x}px;
            top: ${y}px;
            pointer-events: none;
            animation: rippleEffect 600ms ease-out;
        `;

        // Add ripple animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes rippleEffect {
                to {
                    transform: scale(2);
                    opacity: 0;
                }
            }
        `;

        if (!document.querySelector('style[data-ripple]')) {
            style.setAttribute('data-ripple', 'true');
            document.head.appendChild(style);
        }

        button.style.position = 'relative';
        button.style.overflow = 'hidden';
        button.appendChild(ripple);

        setTimeout(() => ripple.remove(), 600);
    });

    // ========================================
    // DROPDOWN SMOOTH TRANSITIONS
    // ========================================

    /**
     * Enhance dropdown menu transitions
     */
    document.querySelectorAll('.dropdown').forEach(dropdown => {
        const menu = dropdown.querySelector('.dropdown-menu');
        if (!menu) return;

        dropdown.addEventListener('show.bs.dropdown', function () {
            menu.style.display = 'block';
            setTimeout(() => menu.classList.add('show'), 10);
        });

        dropdown.addEventListener('hide.bs.dropdown', function () {
            menu.classList.remove('show');
            setTimeout(() => menu.style.display = 'none', 250);
        });
    });

    // ========================================
    // NOTIFICATION BADGE ANIMATION
    // ========================================

    /**
     * Pulse animation for new notifications
     */
    const notificationBadges = document.querySelectorAll('.badge.bg-danger, .badge-count');
    notificationBadges.forEach(badge => {
        if (!prefersReducedMotion && parseInt(badge.textContent) > 0) {
            badge.style.animation = 'countPulse 500ms ease';
        }
    });

    // ========================================
    // PERFORMANCE OPTIMIZATION
    // ========================================

    /**
     * Debounce function for scroll events
     */
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // ========================================
    // LAZY LOADING FOR IMAGES
    // ========================================

    /**
     * Lazy load images for performance
     */
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver(function (entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.classList.add('loaded');
                        imageObserver.unobserve(img);
                    }
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }

    // ========================================
    // EXPORT FOR GLOBAL ACCESS
    // ========================================

    window.ThemeAnimations = {
        prefersReducedMotion,
        animateNumber,
        highlightSearchResults,
        clearSearchHighlights
    };

})();
