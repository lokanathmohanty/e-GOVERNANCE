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
            'dark_mode': 'Dark Mode',
            'high_contrast': 'High Contrast',
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
            'dark_mode': 'डार्क मोड',
            'high_contrast': 'उच्च कंट्रास्ट',
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
            'dark_mode': 'ଡାର୍କ ମୋଡ୍',
            'high_contrast': 'ଉଚ୍ଚ କଣ୍ଟ୍ରାଷ୍ଟ',
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
        // Update displays
        document.querySelectorAll('#text-size-display, #text-size-display-mobile, .text-size-display').forEach(el => {
            el.textContent = `${this.settings.fontSize}%`;
        });
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

        // Update Theme Icons if they exist
        const themeIcons = document.querySelectorAll('#themeIcon, #theme-icon, .theme-icon');
        themeIcons.forEach(icon => {
            if (icon.classList.contains('material-symbols-outlined')) {
                icon.textContent = this.settings.darkMode ? 'light_mode' : 'dark_mode';
            } else if (icon.tagName === 'I') { // Bootstrap Icons
                icon.className = this.settings.darkMode ? 'bi bi-sun-fill' : 'bi bi-moon-fill';
            }
        });
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
        // Font Size controls (Supports IDs and Classes for multiple instances)
        const fontActions = [
            { id: 'btn-increase-text', class: 'btn-increase-text', action: () => this.increaseFont() },
            { id: 'btn-decrease-text', class: 'btn-decrease-text', action: () => this.decreaseFont() },
            { id: 'btn-reset-text', class: 'btn-reset-text', action: () => this.resetFont() },
            { id: 'btn-increase-text-mobile', class: 'btn-increase-text-mobile', action: () => this.increaseFont() },
            { id: 'btn-decrease-text-mobile', class: 'btn-decrease-text-mobile', action: () => this.decreaseFont() }
        ];

        fontActions.forEach(item => {
            const el = document.getElementById(item.id);
            if (el) el.addEventListener('click', (e) => {
                e.stopPropagation();
                item.action();
            });
            document.querySelectorAll(`.${item.class}`).forEach(btn => {
                if (btn !== el) btn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    item.action();
                });
            });
        });

        // Toggle Sync Helper
        const bindToggles = (type, idArr, classArr, stateKey, onApply) => {
            const elements = new Set();
            idArr.forEach(id => {
                const el = document.getElementById(id);
                if (el) elements.add(el);
            });
            classArr.forEach(cls => {
                document.querySelectorAll(`.${cls}`).forEach(el => elements.add(el));
            });

            elements.forEach(toggle => {
                toggle.checked = this.settings[stateKey];
                toggle.addEventListener('change', (e) => {
                    e.stopPropagation();
                    this.settings[stateKey] = e.target.checked;
                    this.saveSettings();
                    onApply();
                    // Sync all other toggles of the same type
                    elements.forEach(other => {
                        if (other !== e.target) other.checked = e.target.checked;
                    });
                });
                // Also stop click propagation for the parent label/div
                toggle.addEventListener('click', (e) => e.stopPropagation());
            });
        };

        // High Contrast
        bindToggles(
            'high-contrast',
            ['cb-high-contrast', 'cb-high-contrast-mobile'],
            ['cb-high-contrast'],
            'highContrast',
            () => this.applyTheme()
        );

        // Dark Mode
        bindToggles(
            'dark-mode',
            ['cb-dark-mode', 'cb-dark-mode-mobile'],
            ['cb-dark-mode', 'theme-toggle-cb'],
            'darkMode',
            () => this.applyTheme()
        );

        // Language Select Sync
        const langSelectors = new Set();
        ['language-select', 'language-select-mobile'].forEach(id => {
            const el = document.getElementById(id);
            if (el) langSelectors.add(el);
        });
        document.querySelectorAll('.language-select').forEach(el => langSelectors.add(el));

        langSelectors.forEach(select => {
            select.value = this.settings.language;
            select.addEventListener('change', (e) => {
                e.stopPropagation();
                const lang = e.target.value;
                this.setLanguage(lang);
                // Sync others
                langSelectors.forEach(other => {
                    if (other !== e.target) other.value = lang;
                });
            });
            select.addEventListener('click', (e) => e.stopPropagation());
        });
    }
};

// Global initialization
document.addEventListener('DOMContentLoaded', () => {
    // Initialize the manager
    AccessibilityManager.init();

    // Assign to window for global access
    window.accessibilityManager = AccessibilityManager;

    // Quick theme toggle helper for specific simple buttons if needed
    const themeBtns = document.querySelectorAll('#theme-toggle, #themeToggle, .theme-toggle');
    themeBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            const isDark = document.documentElement.classList.contains('dark');
            AccessibilityManager.settings.darkMode = !isDark;
            AccessibilityManager.saveSettings();
            AccessibilityManager.applyTheme();

            // Sync all related toggle switches
            document.querySelectorAll('#cb-dark-mode, #cb-dark-mode-mobile, .cb-dark-mode').forEach(cb => {
                cb.checked = !isDark;
            });
        });
    });
});
