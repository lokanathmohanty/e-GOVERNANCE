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
                'notifications.no_new': 'No new notifications',

                // Hero Section
                'hero.title': 'e-Governance Service Management System',
                'hero.subtitle': 'Secure, transparent citizen services. Empowering the state with a robust digital platform for all administrative needs.',
                'hero.official': 'Official Govt Portal',
                'hero.login_citizen': 'Citizen Login',
                'hero.login_officer': 'Officer Login',
                'hero.cta': 'Apply for Services',

                // Emergency Bar
                'em.police': 'Police',
                'em.ambulance': 'Ambulance',
                'em.fire': 'Fire',
                'em.women': 'Women Helpline',

                // Cards
                'card.apply': 'Apply for Services',
                'card.apply.desc': 'Submit applications for certificates, welfare schemes, and licenses safely from your home.',
                'card.apply.btn': 'Start Application',
                'card.track': 'Track Status',
                'card.track.desc': 'Real-time tracking of your application workflow, approvals, and current pending status.',
                'card.track.btn': 'Check Status',
                'card.grievance': 'Raise Grievance',
                'card.grievance.desc': 'Lodge complaints regarding civic issues and track their resolution with our transparent system.',
                'card.grievance.btn': 'File Complaint',

                // How it Works
                'how.title': 'How It Works',
                'how.subtitle': 'Understanding the lifecycle of your application. We believe in complete transparency at every step.',
                'step.1': 'Apply Online',
                'step.1.desc': 'Submit your application with unified KYC verification.',
                'step.2': 'Verification',
                'step.2.desc': 'Field Officer verifies docs & eligibility criteria.',
                'step.3': 'Approval',
                'step.3.desc': 'Final scrutiny & digital signing by authority.',
                'step.4': 'Delivered',
                'step.4.desc': 'Certificate issued to your secure digital locker.',

                // Impact Dashboard
                'impact.title': 'Live Impact Dashboard',
                'impact.subtitle': 'Real-time metrics demonstrating our commitment to efficiency and transparency in public administration.',
                'stats.total': 'Applications Processed',
                'stats.issued': 'Certificates Issued',
                'stats.days': 'Avg Processing Time',
                'stats.satisfaction': 'Citizen Satisfaction',

                // Verification
                'verify.title': 'Check Certificate Authenticity',
                'verify.subtitle': 'Employers, schools, and agencies can verify the validity of any document issued by this portal instantly.',
                'verify.placeholder': 'Enter Application ID (e.g., APP12345)',
                'verify.btn': 'Verify Now',

                // Announcements
                'news.title': 'Announcements & Updates',
                'news.subtitle': 'Stay informed about latest policies, download circulars, and check deadlines.',
                'tab.news': 'Latest News',
                'tab.notices': 'Circulars & Notices',

                // Stories
                'stories.title': 'What Citizens Say',

                // Key Benefits
                'benefits.title': 'Key Benefits',
                'benefits.subtitle': 'Our platform is built on pillars of security, accountability, and efficiency to serve you better.'
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
                'notifications.no_new': 'कोई नई सूचना नहीं',

                // Hero Section
                'hero.title': 'ई-गवर्नेंस सेवा प्रबंधन प्रणाली',
                'hero.subtitle': 'सुरक्षित, पारदर्शी नागरिक सेवाएं। सभी प्रशासनिक आवश्यकताओं के लिए एक मजबूत डिजिटल प्लेटफॉर्म के साथ राज्य को सशक्त बनाना।',
                'hero.official': 'आधिकारिक सरकारी पोर्टल',
                'hero.login_citizen': 'नागरिक लॉगिन',
                'hero.login_officer': 'अधिकारी लॉगिन',
                'hero.cta': 'सेवाओं के लिए आवेदन करें',

                // Emergency Bar
                'em.police': 'पुलिस',
                'em.ambulance': 'एम्बुलेंस',
                'em.fire': 'फायर ब्रिगेड',
                'em.women': 'महिला हेल्पलाइन',

                // Cards
                'card.apply': 'सेवाओं के लिए आवेदन करें',
                'card.apply.desc': 'घर बैठे प्रमाण पत्र, कल्याणकारी योजनाओं और लाइसेंस के लिए आवेदन जमा करें।',
                'card.apply.btn': 'आवेदन शुरू करें',
                'card.track': 'स्थिति ट्रैक करें',
                'card.track.desc': 'अपने आवेदन के कार्यप्रवाह, अनुमोदन और वर्तमान लंबित स्थिति की रीयल-टाइम ट्रैकिंग।',
                'card.track.btn': 'स्थिति जांचें',
                'card.grievance': 'शिकायत दर्ज करें',
                'card.grievance.desc': 'नागरिक मुद्दों के संबंध में शिकायत दर्ज करें और हमारी पारदर्शी प्रणाली के साथ उनके समाधान को ट्रैक करें।',
                'card.grievance.btn': 'शिकायत दर्ज करें',

                // How it Works
                'how.title': 'यह कैसे काम करता है',
                'how.subtitle': 'अपने आवेदन के जीवनचक्र को समझें। हम हर कदम पर पूर्ण पारदर्शिता में विश्वास करते हैं।',
                'step.1': 'ऑनलाइन आवेदन करें',
                'step.1.desc': 'एकीकृत केवाईसी सत्यापन के साथ अपना आवेदन जमा करें।',
                'step.2': 'सत्यापन',
                'step.2.desc': 'क्षेत्र अधिकारी दस्तावेजों और पात्रता मापदंडों का सत्यापन करता है।',
                'step.3': 'अनुमोदन',
                'step.3.desc': 'प्राधिकरण द्वारा अंतिम जांच और डिजिटल हस्ताक्षर।',
                'step.4': 'वितरण',
                'step.4.desc': 'आपके सुरक्षित डिजिटल लॉकर में प्रमाण पत्र जारी किया जाता है।',

                // Impact Dashboard
                'impact.title': 'लाइव प्रभाव डैशबोर्ड',
                'impact.subtitle': 'सार्वजनिक प्रशासन में दक्षता और पारदर्शिता के प्रति हमारी प्रतिबद्धता को प्रदर्शित करने वाले रीयल-टाइम मेट्रिक्स।',
                'stats.total': 'कुल आवेदन संसाधित',
                'stats.issued': 'प्रमाणपत्र जारी किए गए',
                'stats.days': 'औसत प्रसंस्करण समय',
                'stats.satisfaction': 'नागरिक संतुष्टि',

                // Verification
                'verify.title': 'प्रमाणपत्र की प्रामाणिकता जांचें',
                'verify.subtitle': 'नियोक्ता और एजेंसियां इस पोर्टल द्वारा जारी किसी भी दस्तावेज की वैधता की तुरंत जांच कर सकते हैं।',
                'verify.placeholder': 'आवेदन आईडी दर्ज करें (उदा. APP12345)',
                'verify.btn': 'अभी सत्यापित करें',

                // Announcements
                'news.title': 'घोषणाएं और अपडेट',
                'news.subtitle': 'नवीनतम नीतियों के बारे में सूचित रहें, परिपत्र डाउनलोड करें और समय सीमा जांचें।',
                'tab.news': 'ताज़ा खबर',
                'tab.notices': 'परिपत्र और नोटिस',

                // Stories
                'stories.title': 'नागरिक क्या कहते हैं',

                // Key Benefits
                'benefits.title': 'मुख्य लाभ',
                'benefits.subtitle': 'हमारा मंच आपको बेहतर सेवा देने के लिए सुरक्षा, जवाबदेही और दक्षता के स्तंभों पर बना है।'
            },
            or: {
                'nav.home': 'ମୁଖ୍ୟ ପୃଷ୍ଠା',
                'nav.services': 'ସେବା',
                'nav.grievance': 'ଅଭିଯୋଗ',
                'nav.contact': 'ଯୋଗାଯୋଗ',
                'nav.dashboard': 'ଡ୍ୟାସବୋର୍ଡ',
                'nav.locker': 'ଲକର',
                'nav.login': 'ନାଗରିକ ଲଗଇନ୍',
                'nav.logout': 'ଲଗଆଉଟ୍',
                'footer.about': 'ପୋର୍ଟାଲ୍ ବିଷୟରେ',
                'footer.services': 'ସେବା ତାଲିକା',
                'footer.help': 'ସାହାଯ୍ୟ ଏବଂ PDF',
                'footer.manuals': 'ବ୍ୟବହାରକାରୀ ମାନୁଆଲ୍',
                'footer.contact': 'ସହାୟତା ଯୋଗାଯୋଗ',
                'footer.privacy': 'ଗୋପନୀୟତା ନୀତି',
                'footer.terms': 'ବ୍ୟବହାର ନିୟମାବଳୀ',
                'footer.accessibility': 'ପ୍ରବେଶଯୋଗ୍ୟତା',
                'accessibility.font_size': 'ଅକ୍ଷର ଆକାର',
                'accessibility.contrast': 'ହାଇ କଣ୍ଟ୍ରାଷ୍ଟ',
                'accessibility.language': 'ଭାଷା',
                'notifications.title': 'ବିଜ୍ଞପ୍ତି',
                'notifications.mark_all': 'ସମସ୍ତ ପଢାଯାଇଛି',
                'notifications.view_all': 'ସମସ୍ତ ଇତିହାସ ଦେଖନ୍ତୁ',
                'notifications.no_new': 'କୌଣସି ନୂତନ ବିଜ୍ଞପ୍ତି ନାହିଁ',

                // Hero Section
                'hero.title': 'ଇ-ଶାସନ ସେବା ପରିଚାଳନା ପ୍ରଣାଳୀ',
                'hero.subtitle': 'ସୁରକ୍ଷିତ, ସ୍ୱଚ୍ଛ ନାଗରିକ ସେବା | ସମସ୍ତ ପ୍ରଶାସନିକ ଆବଶ୍ୟକତା ପାଇଁ ଏକ ଦୃଢ ଡିଜିଟାଲ୍ ପ୍ଲାଟଫର୍ମ ସହିତ ରାଜ୍ୟକୁ ସଶକ୍ତ କରିବା |',
                'hero.official': 'ଅଫିସିଆଲ୍ ସରକାରୀ ପୋର୍ଟାଲ୍',
                'hero.login_citizen': 'ନାଗରିକ ଲଗଇନ୍',
                'hero.login_officer': 'ଅଧିକାରୀ ଲଗଇନ୍',
                'hero.cta': 'ସେବା ପାଇଁ ଆବେଦନ କରନ୍ତୁ',

                // Emergency Bar
                'em.police': 'ପୋଲିସ',
                'em.ambulance': 'ଆମ୍ବୁଲାନ୍ସ',
                'em.fire': 'ଅଗ୍ନିଶମ ବାହିନୀ',
                'em.women': 'ମହିଳା ହେଲ୍ପଲାଇନ',

                // Cards
                'card.apply': 'ସେବା ପାଇଁ ଆବେଦନ କରନ୍ତୁ',
                'card.apply.desc': 'ଘରେ ବସି ପ୍ରମାଣପତ୍ର, କଲ୍ୟାଣକାରୀ ଯୋଜନା ଏବଂ ଲାଇସେନ୍ସ ପାଇଁ ଆବେଦନ ଦାଖଲ କରନ୍ତୁ |',
                'card.apply.btn': 'ଆବେଦନ ଆରମ୍ଭ କରନ୍ତୁ',
                'card.track': 'ସ୍ଥିତି ଯାଞ୍ଚ କରନ୍ତୁ',
                'card.track.desc': 'ଆପଣଙ୍କ ଆବେଦନ କାର୍ଯ୍ୟ ପ୍ରବାହ, ଅନୁମୋଦନ ଏବଂ ବର୍ତ୍ତମାନର ବିଚାରାଧୀନ ସ୍ଥିତିର ରିଅଲ୍-ଟାଇମ୍ ଟ୍ରାକିଂ |',
                'card.track.btn': 'ସ୍ଥିତି ଦେଖନ୍ତୁ',
                'card.grievance': 'ଅଭିଯୋଗ କରନ୍ତୁ',
                'card.grievance.desc': 'ନାଗରିକ ସମସ୍ୟା ସମ୍ପର୍କରେ ଅଭିଯୋଗ ଦାଖଲ କରନ୍ତୁ ଏବଂ ଆମର ସ୍ୱଚ୍ଛ ପ୍ରଣାଳୀ ସହିତ ସେଗୁଡିକର ସମାଧାନ ଟ୍ରାକ୍ କରନ୍ତୁ |',
                'card.grievance.btn': 'ଅଭିଯୋଗ ଦାଖଲ କରନ୍ତୁ',

                // How it Works
                'how.title': 'କିପରି କାର୍ଯ୍ୟ କରେ',
                'how.subtitle': 'ଆପଣଙ୍କ ଆବେଦନ ପ୍ରକ୍ରିୟା ବୁଝନ୍ତୁ। ଆମେ ପ୍ରତ୍ୟେକ ପଦକ୍ଷେପରେ ସମ୍ପୂର୍ଣ୍ଣ ସ୍ୱଚ୍ଛତାରେ ବିଶ୍ୱାସ କରୁ।',
                'step.1': 'ଅନ୍‌ଲାଇନ୍ ଆବେଦନ',
                'step.1.desc': 'ଏକୀକୃତ KYC ଯାଞ୍ଚ ସହିତ ଆପଣଙ୍କର ଆବେଦନ ଦାଖଲ କରନ୍ତୁ।',
                'step.2': 'ଯାଞ୍ଚ',
                'step.2.desc': 'କ୍ଷେତ୍ର ଅଧିକାରୀ ଦଲିଲ୍ ଏବଂ ଯୋଗ୍ୟତା ମାନଦଣ୍ଡ ଯାଞ୍ଚ କରନ୍ତି।',
                'step.3': 'ଅନୁମୋଦନ',
                'step.3.desc': 'କର୍ତ୍ତୃପକ୍ଷଙ୍କ ଦ୍ୱାରା ଚୂଡ଼ାନ୍ତ ଯାଞ୍ଚ ଏବଂ ଡିଜିଟାଲ୍ ଦସ୍ତଖତ।',
                'step.4': 'ବିତରଣ',
                'step.4.desc': 'ଆପଣଙ୍କ ସୁରକ୍ଷିତ ଡିଜିଟାଲ୍ ଲକର୍ ରେ ପ୍ରମାଣପତ୍ର ଜାରି କରାଯାଏ।',

                // Impact Dashboard
                'impact.title': 'ଲାଇଭ୍ ପ୍ରଭାବ ଡ୍ୟାସବୋର୍ଡ',
                'impact.subtitle': 'ସର୍ବସାଧାରଣ ପ୍ରଶାସନରେ ଦକ୍ଷତା ଏବଂ ସ୍ୱଚ୍ଛତା ପ୍ରତି ଆମର ପ୍ରତିବଦ୍ଧତା ପ୍ରଦର୍ଶନ କରୁଥିବା ରିଅଲ୍-ଟାଇମ୍ ମେଟ୍ରିକ୍ସ।',
                'stats.total': 'ଆବେଦନ ପ୍ରକ୍ରିୟାକରଣ',
                'stats.issued': 'ପ୍ରମାଣପତ୍ର ଜାରି',
                'stats.days': 'ହାରାହାରି ପ୍ରକ୍ରିୟାକରଣ ସମୟ',
                'stats.satisfaction': 'ନାଗରିକ ସନ୍ତୁଷ୍ଟି',

                // Verification
                'verify.title': 'ପ୍ରମାଣପତ୍ର ସତ୍ୟତା ଯାଞ୍ଚ',
                'verify.subtitle': 'ନିଯୁକ୍ତିଦାତା ଏବଂ ସଂସ୍ଥାଗୁଡ଼ିକ ଏହି ପୋର୍ଟାଲ୍ ଦ୍ୱାରା ଜାରି କରାଯାଇଥିବା ଯେକୌଣସି ଦଲିଲର ବୈଧତା ତୁରନ୍ତ ଯାଞ୍ଚ କରିପାରିବେ।',
                'verify.placeholder': 'ଆବେଦନ ଆଇଡି ପ୍ରବେଶ କରନ୍ତୁ (ଉଦାହରଣ APP12345)',
                'verify.btn': 'ବର୍ତ୍ତମାନ ଯାଞ୍ଚ କରନ୍ତୁ',

                // Announcements
                'news.title': 'ଘୋଷଣା ଏବଂ ଅଦ୍ୟତନ',
                'news.subtitle': 'ସର୍ବଶେଷ ନୀତି ବିଷୟରେ ଅବଗତ ରୁହନ୍ତୁ, ସର୍କୁଲାର୍ ଡାଉନଲୋଡ୍ କରନ୍ତୁ ଏବଂ ସମୟସୀମା ଯାଞ୍ଚ କରନ୍ତୁ |',
                'tab.news': 'ସର୍ବଶେଷ ଖବର',
                'tab.notices': 'ସର୍କୁଲାର୍ ଏବଂ ନୋଟିସ୍',

                // Stories
                'stories.title': 'ନାଗରିକଙ୍କ ମତାମତ',

                // Key Benefits
                'benefits.title': 'ମୁଖ୍ୟ ଲାଭ',
                'benefits.subtitle': 'ଆପଣଙ୍କୁ ଉତ୍ତମ ସେବା ଯୋଗାଇବା ପାଇଁ ଆମର ପ୍ଲାଟଫର୍ମ ସୁରକ୍ଷା, ଉତ୍ତରଦାୟିତ୍ୱ ଏବଂ ଦକ୍ଷତା ଉପରେ ଆଧାରିତ।'
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
