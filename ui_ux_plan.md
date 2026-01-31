# e-Governance UI/UX Redesign Plan

## 1. Design System Foundation
- [ ] Define shared CSS variables in a new `static/css/design_system.css` (re-creating it better).
- [ ] Typography: Use `Inter` for body and `Public Sans` for headings.
- [ ] Colors: 
  - Primary: `#D97706` (Saffron)
  - Secondary: `#1E293B` (Navy)
  - Surface: `#F8FAFC`
  - Success: `#059669`
- [ ] Components: `.btn-premium`, `.card-premium`, `.input-premium`.

## 2. Global Base Templates (`base.html` & `base_bootstrap.html`)
- [ ] Consistent Navbar branding.
- [ ] Mobile navigation: Implement a slide-right drawer for mobile menus.
- [ ] Responsive footer with stacked links on mobile.

## 3. Homepage (`home.html`)
- [ ] Hero Section: Improve text leading/tracking and image scaling.
- [ ] Service Category Grid: Perfect 1/2/4 column responsiveness.
- [ ] Footer: Modernized layouts and Social icons.

## 4. Dashboards (Citizen, Officer, Head, Admin)
- [ ] Standardized Stats Cards.
- [ ] Responsive Tables: Card-based fallback for very small screens.
- [ ] Chart Containers: Responsive aspect ratios.

## 5. Account Pages (Login/Register/Profile)
- [ ] Split-screen layouts for Login/Register on Desktop.
- [ ] Full-width stacked for Mobile.
