/**
 * Accessibility Manager
 * Handles font size, contrast, and language preferences
 */

class AccessibilityManager {
    constructor() {
        this.fontSizes = {
            small: 0.875,
            normal: 1,
            large: 1.125,
            xlarge: 1.25
        };
        this.currentFontSize = 'normal';
        this.highContrast = false;
        this.currentLanguage = 'en';

        this.init();
    }

    init() {
        // Load saved preferences
        this.loadPreferences();

        // Apply saved settings
        this.applyFontSize();
        this.applyContrast();
        this.applyLanguage();

        // Setup event listeners
        this.setupEventListeners();
    }

    loadPreferences() {
        this.currentFontSize = localStorage.getItem('fontSize') || 'normal';
        this.highContrast = localStorage.getItem('highContrast') === 'true';
        this.currentLanguage = localStorage.getItem('language') || 'en';
    }

    setupEventListeners() {
        // Font size controls
        const fontSizeButtons = document.querySelectorAll('[data-font-size]');
        fontSizeButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const size = e.currentTarget.dataset.fontSize;
                this.setFontSize(size);
            });
        });

        // Contrast toggle
        const contrastToggle = document.getElementById('contrastToggle');
        if (contrastToggle) {
            contrastToggle.addEventListener('click', () => {
                this.toggleContrast();
            });
        }

        // Language selector
        const languageSelect = document.getElementById('languageSelect');
        if (languageSelect) {
            languageSelect.addEventListener('change', (e) => {
                this.setLanguage(e.target.value);
            });
        }
    }

    setFontSize(size) {
        if (!this.fontSizes[size]) return;

        this.currentFontSize = size;
        localStorage.setItem('fontSize', size);
        this.applyFontSize();

        // Update active state
        document.querySelectorAll('[data-font-size]').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.fontSize === size);
        });
    }

    applyFontSize() {
        const multiplier = this.fontSizes[this.currentFontSize];
        document.documentElement.style.fontSize = `${multiplier * 16}px`;

        // Update active button state
        document.querySelectorAll('[data-font-size]').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.fontSize === this.currentFontSize);
        });
    }

    toggleContrast() {
        this.highContrast = !this.highContrast;
        localStorage.setItem('highContrast', this.highContrast);
        this.applyContrast();
    }

    applyContrast() {
        if (this.highContrast) {
            document.documentElement.classList.add('high-contrast');
        } else {
            document.documentElement.classList.remove('high-contrast');
        }

        // Update button icon
        const contrastIcon = document.getElementById('contrastIcon');
        if (contrastIcon) {
            contrastIcon.textContent = this.highContrast ? 'contrast' : 'contrast';
        }
    }

    setLanguage(lang) {
        this.currentLanguage = lang;
        localStorage.setItem('language', lang);
        this.applyLanguage();
    }

    applyLanguage() {
        // Update language selector
        const languageSelect = document.getElementById('languageSelect');
        if (languageSelect) {
            languageSelect.value = this.currentLanguage;
        }

        // Translate page content
        this.translatePage();
    }

    translatePage() {
        const elements = document.querySelectorAll('[data-i18n]');
        elements.forEach(element => {
            const key = element.dataset.i18n;
            const translation = this.getTranslation(key);
            if (translation) {
                if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
                    element.placeholder = translation;
                } else {
                    element.textContent = translation;
                }
            }
        });
    }

    getTranslation(key) {
        const translations = {
            en: {
                'nav.home': 'Home',
                'nav.services': 'Services',
                'nav.grievance': 'Grievance',
                'nav.contact': 'Contact Us',
                'nav.dashboard': 'Dashboard',
                'nav.locker': 'Locker',
                'nav.login': 'Citizen Login',
                'nav.logout': 'Logout',
                'footer.about': 'About Portal',
                'footer.services': 'Services List',
                'footer.help': 'Help & PDF',
                'footer.manuals': 'User Manuals',
                'footer.contact': 'Contact Support',
                'footer.privacy': 'Privacy Policy',
                'footer.terms': 'Terms of Use',
                'footer.accessibility': 'Accessibility',
                'accessibility.font_size': 'Font Size',
                'accessibility.contrast': 'High Contrast',
                'accessibility.language': 'Language',
                'notifications.title': 'Notifications',
                'notifications.mark_all': 'Mark all read',
                'notifications.view_all': 'View All History',
                'notifications.no_new': 'No new notifications'
            },
            hi: {
                'nav.home': 'होम',
                'nav.services': 'सेवाएं',
                'nav.grievance': 'शिकायत',
                'nav.contact': 'संपर्क करें',
                'nav.dashboard': 'डैशबोर्ड',
                'nav.locker': 'लॉकर',
                'nav.login': 'नागरिक लॉगिन',
                'nav.logout': 'लॉगआउट',
                'footer.about': 'पोर्टल के बारे में',
                'footer.services': 'सेवाओं की सूची',
                'footer.help': 'सहायता और PDF',
                'footer.manuals': 'उपयोगकर्ता मैनुअल',
                'footer.contact': 'संपर्क सहायता',
                'footer.privacy': 'गोपनीयता नीति',
                'footer.terms': 'उपयोग की शर्तें',
                'footer.accessibility': 'पहुंच',
                'accessibility.font_size': 'फ़ॉन्ट आकार',
                'accessibility.contrast': 'उच्च कंट्रास्ट',
                'accessibility.language': 'भाषा',
                'notifications.title': 'सूचनाएं',
                'notifications.mark_all': 'सभी को पढ़ा हुआ चिह्नित करें',
                'notifications.view_all': 'सभी इतिहास देखें',
                'notifications.no_new': 'कोई नई सूचना नहीं'
            },
            es: {
                'nav.home': 'Inicio',
                'nav.services': 'Servicios',
                'nav.grievance': 'Queja',
                'nav.contact': 'Contáctenos',
                'nav.dashboard': 'Panel',
                'nav.locker': 'Casillero',
                'nav.login': 'Inicio de sesión ciudadano',
                'nav.logout': 'Cerrar sesión',
                'footer.about': 'Acerca del portal',
                'footer.services': 'Lista de servicios',
                'footer.help': 'Ayuda y PDF',
                'footer.manuals': 'Manuales de usuario',
                'footer.contact': 'Contactar soporte',
                'footer.privacy': 'Política de privacidad',
                'footer.terms': 'Términos de uso',
                'footer.accessibility': 'Accesibilidad',
                'accessibility.font_size': 'Tamaño de fuente',
                'accessibility.contrast': 'Alto contraste',
                'accessibility.language': 'Idioma',
                'notifications.title': 'Notificaciones',
                'notifications.mark_all': 'Marcar todo como leído',
                'notifications.view_all': 'Ver todo el historial',
                'notifications.no_new': 'No hay nuevas notificaciones'
            }
        };

        return translations[this.currentLanguage]?.[key] || null;
    }

    // Public method to get current settings
    getSettings() {
        return {
            fontSize: this.currentFontSize,
            highContrast: this.highContrast,
            language: this.currentLanguage
        };
    }
}

// Initialize on page load
let accessibilityManager;
document.addEventListener('DOMContentLoaded', () => {
    accessibilityManager = new AccessibilityManager();
});
