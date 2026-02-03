/**
 * Accessibility & Localization Manager
 * Handles text sizing, high contrast, dark mode, and client-side translations.
 */

const AccessibilityManager = {
    settings: {
        fontSize: 100,
        highContrast: false,
        darkMode: false,
        language: 'en'
    },

    translations: {
        'en': {
            'home': 'Home', 'services': 'Services', 'contact': 'Contact Us',
            'dashboard': 'My Dashboard', 'officer_console': 'Officer Console',
            'analytics': 'Analytics', 'login': 'Login', 'logout': 'Logout',
            'profile': 'My Profile', 'search': 'Search', 'notifications': 'Notifications',
            'accessibility': 'Accessibility', 'text_size': 'Text Size',
            'theme': 'Theme', 'language': 'Language', 'reset': 'Reset', 'welcome': 'Welcome',
            'em.police': 'Police', 'em.ambulance': 'Ambulance', 'em.women': 'Women', 'em.fire': 'Fire',
            'hero.title': 'e-Governance Service Management System',
            'hero.subtitle': 'Secure, transparent citizen services. Empowering the state with a robust digital platform for all administrative needs.',
            'hero.cta': 'Apply for Services', 'nav.login': 'Citizen Login', 'nav.services': 'Citizen Services',
            'nav.home': 'Home', 'nav.grievance': 'Grievance', 'nav.contact': 'Contact Us',
            'card.apply': 'Apply for Services', 'card.apply.desc': 'Submit applications for certificates, welfare schemes, and licenses safely from your home.',
            'card.apply.btn': 'Start Application', 'card.track': 'Track Status', 'card.track.desc': 'Real-time tracking of your application workflow, approvals, and current pending status.',
            'card.track.btn': 'Check Status', 'card.grievance': 'Raise Grievance', 'card.grievance.desc': 'Lodge complaints regarding civic issues and track their resolution with our transparent system.',
            'card.grievance.btn': 'File Complaint', 'how.title': 'How It Works', 'how.subtitle': 'Understanding the lifecycle of your application. We believe in complete transparency at every step.',
            'step.1': 'Apply Online', 'step.1.desc': 'Submit your application with unified KYC verification.',
            'step.2': 'Verification', 'step.2.desc': 'Field Officer verifies docs & eligibility criteria.',
            'step.3': 'Approval', 'step.3.desc': 'Final scrutiny & digital signing by authority.',
            'step.4': 'Issuance', 'step.4.desc': 'Get your digital certificate instantly.'
        },
        'hi': {
            'home': 'मुखपृष्ठ', 'services': 'सेवाएं', 'contact': 'संपर्क करें',
            'dashboard': 'मेरा डैशबोर्ड', 'officer_console': 'अधिकारी कंसोल',
            'analytics': 'विश्लेषण', 'login': 'लॉगिन', 'logout': 'लॉग आउट',
            'profile': 'मेरी प्रोफाइल', 'search': 'खोजें', 'notifications': 'सूचनाएं',
            'accessibility': 'पहुंच-योग्यता', 'text_size': 'लेख का आकार',
            'theme': 'थीम', 'language': 'भाषा', 'reset': 'रीसेट', 'welcome': 'स्वागत',
            'em.police': 'पुलिस', 'em.ambulance': 'एम्बुलेंस', 'em.women': 'महिला', 'em.fire': 'दमकल',
            'hero.title': 'ई-गवर्नेंस सेवा प्रबंधन प्रणाली',
            'hero.subtitle': 'सुरक्षित, पारदर्शी नागरिक सेवाएं। सभी प्रशासनिक आवश्यकताओं के लिए एक मजबूत डिजिटल प्लेटफॉर्म के साथ राज्य को सशक्त बनाना।',
            'hero.cta': 'सेवाओं के लिए आवेदन करें', 'nav.login': 'नागरिक लॉगिन', 'nav.services': 'नागरिक सेवाएं',
            'nav.home': 'मुखपृष्ठ', 'nav.grievance': 'शिकायत', 'nav.contact': 'संपर्क करें',
            'card.apply': 'सेवाओं के लिए आवेदन करें', 'card.apply.desc': 'अपने घर से सुरक्षित रूप से प्रमाण पत्र, कल्याणकारी योजनाओं और लाइसेंस के लिए आवेदन जमा करें।',
            'card.apply.btn': 'आवेदन शुरू करें', 'card.track': 'स्थिति ट्रैक करें', 'card.track.desc': 'आपके आवेदन वर्कफ़्लो, अनुमोदन और वर्तमान लंबित स्थिति की रीयल-टाइम ट्रैकिंग।',
            'card.track.btn': 'स्थिति जांचें', 'card.grievance': 'शिकायत दर्ज करें', 'card.grievance.desc': 'नागरिक मुद्दों के संबंध में शिकायतें दर्ज करें और हमारे पारदर्शी सिस्टम के साथ उनके समाधान को ट्रैक करें।',
            'card.grievance.btn': 'शिकायत दर्ज करें', 'how.title': 'यह कैसे काम करता है', 'how.subtitle': 'आपके आवेदन के जीवनचक्र को समझना। हम हर कदम पर पूर्ण पारदर्शिता में विश्वास करते हैं।',
            'step.1': 'ऑनलाइन आवेदन करें', 'step.1.desc': 'एकीकृत केवाईसी सत्यापन के साथ अपना आवेदन जमा करें।',
            'step.2': 'सत्यापन', 'step.2.desc': 'क्षेत्र अधिकारी दस्तावेजों और पात्रता मानदंडों की पुष्टि करता है।',
            'step.3': 'अनुमोदन', 'step.3.desc': 'प्राधिकरण द्वारा अंतिम जांच और डिजिटल हस्ताक्षर।',
            'step.4': 'जारी करना', 'step.4.desc': 'अपना डिजिटल प्रमाणपत्र तुरंत प्राप्त करें।'
        },
        'or': {
            'home': 'ମୂଳ ପୃଷ୍ଠା', 'services': 'ସେବା', 'contact': 'ଯୋଗାଯୋଗ',
            'dashboard': 'ମୋର ଡ୍ୟାସବୋର୍ଡ', 'officer_console': 'ଅଧିକାରୀ କନସୋଲ',
            'analytics': 'ବିଶ୍ଳେଷଣ', 'login': 'ଲଗ୍ ଇନ୍', 'logout': 'ଲଗ୍ ଆଉଟ୍',
            'profile': 'ମୋର ପ୍ରୋଫାଇଲ୍', 'search': 'ସନ୍ଧାନ', 'notifications': 'ବିଜ୍ଞପ୍ତି',
            'accessibility': 'ସୁଗମତା', 'text_size': 'ପାଠ୍ୟ ଆକାର',
            'theme': 'ଥିମ୍', 'language': 'ଭାଷା', 'reset': 'ରିସେଟ୍', 'welcome': 'ସ୍ୱାଗତ',
            'em.police': 'ପୋଲିସ', 'em.ambulance': 'ଆମ୍ବୁଲାନ୍ସ', 'em.women': 'ମହିଳା', 'em.fire': 'ଅଗ୍ନିଶମ',
            'hero.title': 'ଇ-ଗଭର୍ଣ୍ଣାନ୍ସ ସେବା ପରିଚାଳନା ପ୍ରଣାଳୀ',
            'hero.subtitle': 'ସୁରକ୍ଷିତ, ସ୍ୱଚ୍ଛ ନାଗରିକ ସେବା | ସମସ୍ତ ପ୍ରଶାସନିକ ଆବଶ୍ୟକତା ପାଇଁ ଏକ ଦୃଢ଼ ଡିଜିଟାଲ୍ ପ୍ଲାଟଫର୍ମ ସହିତ ରାଜ୍ୟକୁ ସଶକ୍ତ କରିବା |',
            'hero.cta': 'ସେବା ପାଇଁ ଆବେଦନ କରନ୍ତୁ', 'nav.login': 'ନାଗରିକ ଲଗଇନ୍', 'nav.services': 'ନାଗରିକ ସେବା',
            'nav.home': 'ମୂଳ ପୃଷ୍ଠା', 'nav.grievance': 'ଅଭିଯୋଗ', 'nav.contact': 'ଯୋଗାଯୋଗ',
            'card.apply': 'ସେବା ପାଇଁ ଆବେଦନ କରନ୍ତୁ', 'card.apply.desc': 'ଆପଣଙ୍କ ଘରୁ ନିରାପଦରେ ପ୍ରମାଣପତ୍ର, କଲ୍ୟାଣକାରୀ ଯୋଜନା ଏବଂ ଲାଇସେନ୍ସ ପାଇଁ ଆବେଦନ ଦାଖଲ କରନ୍ତୁ |',
            'card.apply.btn': 'ଆବେଦନ ଆରମ୍ଭ କରନ୍ତୁ', 'card.track': 'ସ୍ଥିତି ଟ୍ରାକ୍ କରନ୍ତୁ', 'card.track.desc': 'ଆପଣଙ୍କର ଆବେଦନ କାର୍ଯ୍ୟଧାରା, ଅନୁମୋଦନ ଏବଂ ସାମ୍ପ୍ରତିକ ବିଚାରାଧୀନ ସ୍ଥିତିର ରିଅଲ-ଟାଇମ୍ ଟ୍ରାକିଂ |',
            'card.track.btn': 'ସ୍ଥିତି ଯାଞ୍ଚ କରନ୍ତୁ', 'card.grievance': 'ଅଭିଯୋଗ କରନ୍ତୁ', 'card.grievance.desc': 'ନାଗରିକ ସମସ୍ୟା ସମ୍ବନ୍ଧରେ ଅଭିଯୋଗ କରନ୍ତୁ ଏବଂ ଆମର ସ୍ୱଚ୍ଛ ସିଷ୍ଟମ ସହିତ ସେଗୁଡିକର ସମାଧାନ ଟ୍ରାକ୍ କରନ୍ତୁ |',
            'card.grievance.btn': 'ଅଭିଯୋଗ ଦାଖଲ କରନ୍ତୁ', 'how.title': 'ଏହା କିପରି କାମ କରେ', 'how.subtitle': 'ଆପଣଙ୍କର ଆବେଦନର ଜୀବନଚକ୍ରକୁ ବୁଝିବା | ଆମେ ପ୍ରତିଟି ପଦକ୍ଷେପରେ ସମ୍ପୂର୍ଣ୍ଣ ସ୍ୱଚ୍ଛତାରେ ବିଶ୍ୱାସ କରୁ |',
            'step.1': 'ଅନଲାଇନରେ ଆବେଦନ କରନ୍ତୁ', 'step.1.desc': 'ୟୁନିଫାଏଡ୍ KYC ଯାଞ୍ଚ ସହିତ ଆପଣଙ୍କର ଆବେଦନ ଦାଖଲ କରନ୍ତୁ |',
            'step.2': 'ଯାଞ୍ଚ', 'step.2.desc': 'କ୍ଷେତ୍ର ଅଧିକାରୀ ଦଲିଲ ଏବଂ ଯୋଗ୍ୟତା ମାପଦଣ୍ଡ ଯାଞ୍ଚ କରନ୍ତି |',
            'step.3': 'ଅନୁମୋଦନ', 'step.3.desc': 'କର୍ତ୍ତୃପକ୍ଷଙ୍କ ଦ୍ୱାରା ଚୂଡ଼ାନ୍ତ ଯାଞ୍ଚ ଏବଂ ଡିଜିଟାଲ୍ ସ୍ୱାକ୍ଷର |',
            'step.4': 'ପ୍ରଦାନ', 'step.4.desc': 'ତୁରନ୍ତ ଆପଣଙ୍କର ଡିଜିଟାଲ୍ ପ୍ରମାଣପତ୍ର ପାଆନ୍ତୁ |'
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
            try {
                this.settings = { ...this.settings, ...JSON.parse(saved) };
            } catch (e) { console.error("Error parsing settings", e); }
        } else {
            // Legacy fallbacks
            if (localStorage.getItem('data-theme') === 'dark' ||
                (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
                this.settings.darkMode = true;
            }
        }
    },

    saveSettings() {
        localStorage.setItem('accessibility_settings', JSON.stringify(this.settings));
        // Sync with legacy key just in case
        localStorage.setItem('data-theme', this.settings.darkMode ? 'dark' : 'light');
    },

    applySettings() {
        this.applyFontSize();
        this.applyTheme();
        this.applyLanguage();
    },

    applyFontSize() {
        document.documentElement.style.fontSize = `${this.settings.fontSize}%`;
        document.querySelectorAll('#text-size-display, #text-size-display-mobile').forEach(el => {
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

        // Sync all toggles on page
        document.querySelectorAll('#cb-dark-mode, #cb-dark-mode-mobile').forEach(el => el.checked = this.settings.darkMode);
        document.querySelectorAll('#cb-high-contrast, #cb-high-contrast-mobile').forEach(el => el.checked = this.settings.highContrast);

        // Update theme icon if using separate button
        const themeIcon = document.getElementById('themeIcon');
        if (themeIcon) themeIcon.textContent = this.settings.darkMode ? 'light_mode' : 'dark_mode';
    },

    applyLanguage() {
        const langData = this.translations[this.settings.language];
        if (!langData) return;

        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            if (langData[key]) {
                if (el.tagName === 'INPUT' && el.type === 'placeholder') {
                    el.placeholder = langData[key];
                } else {
                    el.textContent = langData[key];
                }
            }
        });

        document.querySelectorAll('#language-select, #language-select-mobile').forEach(el => {
            el.value = this.settings.language;
        });
    },

    bindEvents() {
        // Text Size
        document.querySelectorAll('#btn-increase-text, #btn-increase-text-mobile').forEach(btn => {
            btn.addEventListener('click', () => {
                if (this.settings.fontSize < 150) {
                    this.settings.fontSize += 10;
                    this.saveSettings();
                    this.applyFontSize();
                }
            });
        });

        document.querySelectorAll('#btn-decrease-text, #btn-decrease-text-mobile').forEach(btn => {
            btn.addEventListener('click', () => {
                if (this.settings.fontSize > 70) {
                    this.settings.fontSize -= 10;
                    this.saveSettings();
                    this.applyFontSize();
                }
            });
        });

        document.querySelectorAll('#btn-reset-text').forEach(btn => {
            btn.addEventListener('click', () => {
                this.settings.fontSize = 100;
                this.settings.highContrast = false;
                this.settings.darkMode = false; // Reset to light
                this.saveSettings();
                this.applySettings();
            });
        });

        // Toggles
        document.querySelectorAll('#cb-dark-mode, #cb-dark-mode-mobile, #themeToggle').forEach(el => {
            el.addEventListener('click', (e) => {
                // If it's a checkbox, use its checked state. If it's a button (themeToggle), toggle current state.
                if (el.tagName === 'INPUT') {
                    this.settings.darkMode = el.checked;
                } else {
                    this.settings.darkMode = !this.settings.darkMode;
                }
                this.saveSettings();
                this.applyTheme();
            });
        });

        document.querySelectorAll('#cb-high-contrast, #cb-high-contrast-mobile').forEach(el => {
            el.addEventListener('change', (e) => {
                this.settings.highContrast = e.target.checked;
                this.saveSettings();
                this.applyTheme();
            });
        });

        // Language
        document.querySelectorAll('#language-select, #language-select-mobile').forEach(el => {
            el.addEventListener('change', (e) => {
                this.settings.language = e.target.value;
                this.saveSettings();
                this.applyLanguage();
            });
        });
    }
};

document.addEventListener('DOMContentLoaded', () => AccessibilityManager.init());

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    AccessibilityManager.init();
});
