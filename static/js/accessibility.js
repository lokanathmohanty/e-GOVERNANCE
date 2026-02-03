/**
 * Accessibility & Localization Manager
 * Handles text sizing, high contrast, dark mode, and client-side translations.
 */

const AccessibilityManager = {
    settings: {
        fontSize: 100, // percentage
        highContrast: false,
        darkMode: false,
        language: 'en'
    },

    translations: {
        'en': {
            'home': 'Home',
            'services': 'Services',
            'contact': 'Contact Us',
            'dashboard': 'My Dashboard',
            'officer_console': 'Officer Console',
            'analytics': 'Analytics',
            'login': 'Login',
            'logout': 'Logout',
            'profile': 'My Profile',
            'search': 'Search',
            'notifications': 'Notifications',
            'accessibility': 'Accessibility',
            'text_size': 'Text Size',
            'theme': 'Theme',
            'language': 'Language',
            'reset': 'Reset',
            'welcome': 'Welcome'
        },
        'hi': {
            'home': 'मुखपृष्ठ',
            'services': 'सेवाएं',
            'contact': 'संपर्क करें',
            'dashboard': 'मेरा डैशबोर्ड',
            'officer_console': 'अधिकारी कंसोल',
            'analytics': 'विश्लेषण',
            'login': 'लॉगिन',
            'logout': 'लॉग आउट',
            'profile': 'मेरी प्रोफाइल',
            'search': 'खोजें',
            'notifications': 'सूचनाएं',
            'accessibility': 'पहुंच-योग्यता',
            'text_size': 'लेखा का आकार',
            'theme': 'प्रसंग',
            'language': 'भाषा',
            'reset': 'रीसेट',
            'welcome': 'स्वागत'
        },
        'or': {
            'home': 'ମୂଳ ପୃଷ୍ଠା',
            'services': 'ସେବା',
            'contact': 'ଯୋଗାଯୋଗ',
            'dashboard': 'ମୋର ଡ୍ୟାସବୋର୍ଡ',
            'officer_console': 'ଅଧିକାରୀ କନସୋଲ',
            'analytics': 'ବିଶ୍ଳେଷଣ',
            'login': 'ଲଗ୍ ଇନ୍',
            'logout': 'ଲଗ୍ ଆଉଟ୍',
            'profile': 'ମୋର ପ୍ରୋଫାଇଲ୍',
            'search': 'ସନ୍ଧାନ',
            'notifications': 'ବିଜ୍ଞପ୍ତି',
            'accessibility': 'ସୁଗମତା',
            'text_size': 'ପାଠ୍ୟ ଆକାର',
            'theme': 'ଥିମ୍',
            'language': 'ଭାଷା',
            'reset': 'ରିସେଟ୍',
            'welcome': 'ସ୍ୱାଗତ'
        }
    },

    init() {
        this.loadSettings();
        this.applySettings();
        this.bindEvents();
    },

    loadSettings() {
        const saved = localStorage.getItem('accessibility_settings');
        if (saved) {
            this.settings = { ...this.settings, ...JSON.parse(saved) };
        } else {
            // Check system preference for dark mode
            if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                this.settings.darkMode = true;
            }
        }
    },

    saveSettings() {
        localStorage.setItem('accessibility_settings', JSON.stringify(this.settings));
    },

    applySettings() {
        this.applyFontSize();
        this.applyTheme();
        this.applyLanguage();
    },

    applyFontSize() {
        document.documentElement.style.fontSize = `${this.settings.fontSize}%`;
        // Update display
        const display = document.getElementById('text-size-display');
        if (display) display.textContent = `${this.settings.fontSize}%`;
    },

    applyTheme() {
        const html = document.documentElement;

        // Dark Mode
        if (this.settings.darkMode) {
            html.classList.add('dark');
            html.setAttribute('data-bs-theme', 'dark');
        } else {
            html.classList.remove('dark');
            html.setAttribute('data-bs-theme', 'light');
        }

        // High Contrast
        if (this.settings.highContrast) {
            html.classList.add('high-contrast');
        } else {
            html.classList.remove('high-contrast');
        }
    },

    applyLanguage() {
        // Simple data-i18n replacement
        const elements = document.querySelectorAll('[data-i18n]');
        const langData = this.translations[this.settings.language];

        if (!langData) return;

        elements.forEach(el => {
            const key = el.getAttribute('data-i18n');
            if (langData[key]) {
                if (el.tagName === 'INPUT' && el.type === 'placeholder') {
                    el.placeholder = langData[key];
                } else {
                    el.textContent = langData[key];
                }
            }
        });

        // Update select value
        const langSelect = document.getElementById('language-select');
        if (langSelect) langSelect.value = this.settings.language;
    },

    // Actions
    increaseFont() {
        if (this.settings.fontSize < 150) {
            this.settings.fontSize += 10;
            this.saveSettings();
            this.applyFontSize();
        }
    },

    decreaseFont() {
        if (this.settings.fontSize > 70) {
            this.settings.fontSize -= 10;
            this.saveSettings();
            this.applyFontSize();
        }
    },

    resetFont() {
        this.settings.fontSize = 100;
        this.saveSettings();
        this.applyFontSize();
    },

    toggleHighContrast() {
        this.settings.highContrast = !this.settings.highContrast;
        // High contrast forces light mode usually, unless specific high-contrast-dark exists
        // if (this.settings.highContrast) this.settings.darkMode = false; 
        this.saveSettings();
        this.applyTheme();
    },

    toggleDarkMode() {
        this.settings.darkMode = !this.settings.darkMode;
        this.saveSettings();
        this.applyTheme();
    },

    setLanguage(lang) {
        if (this.translations[lang]) {
            this.settings.language = lang;
            this.saveSettings();
            this.applyLanguage();

            // Optional: If backend language support exists, trigger it here too
            // document.cookie = `django_language=${lang}; path=/`;
        }
    },

    bindEvents() {
        // Text Size (Desktop)
        document.getElementById('btn-increase-text')?.addEventListener('click', () => this.increaseFont());
        document.getElementById('btn-decrease-text')?.addEventListener('click', () => this.decreaseFont());
        document.getElementById('btn-reset-text')?.addEventListener('click', () => this.resetFont());

        // Text Size (Mobile)
        document.getElementById('btn-increase-text-mobile')?.addEventListener('click', () => this.increaseFont());
        document.getElementById('btn-decrease-text-mobile')?.addEventListener('click', () => this.decreaseFont());

        // High Contrast
        const bindHighContrast = (id) => {
            const toggle = document.getElementById(id);
            if (toggle) {
                toggle.checked = this.settings.highContrast;
                toggle.addEventListener('change', (e) => {
                    this.settings.highContrast = e.target.checked;
                    this.saveSettings();
                    this.applyTheme();
                    // Sync
                    const otherId = id === 'cb-high-contrast' ? 'cb-high-contrast-mobile' : 'cb-high-contrast';
                    const other = document.getElementById(otherId);
                    if (other) other.checked = e.target.checked;
                });
            }
        };
        bindHighContrast('cb-high-contrast');
        bindHighContrast('cb-high-contrast-mobile');

        // Dark Mode
        const bindDarkMode = (id) => {
            const toggle = document.getElementById(id);
            if (toggle) {
                toggle.checked = this.settings.darkMode;
                toggle.addEventListener('change', (e) => {
                    this.settings.darkMode = e.target.checked;
                    this.saveSettings();
                    this.applyTheme();
                    // Sync other toggles
                    const otherId = id === 'cb-dark-mode' ? 'cb-dark-mode-mobile' : 'cb-dark-mode';
                    const other = document.getElementById(otherId);
                    if (other) other.checked = e.target.checked;
                });
            }
        };
        bindDarkMode('cb-dark-mode');
        bindDarkMode('cb-dark-mode-mobile');

        // Language
        const bindLanguage = (id) => {
            const select = document.getElementById(id);
            if (select) {
                select.value = this.settings.language;
                select.addEventListener('change', (e) => {
                    this.setLanguage(e.target.value);
                    // Sync other
                    const otherId = id === 'language-select' ? 'language-select-mobile' : 'language-select';
                    const other = document.getElementById(otherId);
                    if (other) other.value = e.target.value;
                });
            }
        };
        bindLanguage('language-select');
        bindLanguage('language-select-mobile');
    }
};

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    AccessibilityManager.init();
});
