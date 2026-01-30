---
description: Migrate from Tailwind to Bootstrap 5 and align with 3-tier architecture
---

# Bootstrap 5 Migration & Architecture Alignment Workflow

## Overview
This workflow restructures the e-Governance MIS system to strictly follow the specified 3-tier architecture with Bootstrap 5, MySQL, and proper RBAC.

## Step 1: Update Base Template with Bootstrap 5
- Remove Tailwind CDN from `templates/base.html`
- Add Bootstrap 5.3 CDN links
- Update navbar to use Bootstrap components
- Ensure responsive mobile menu

## Step 2: Update All Templates
- `templates/home.html` - Landing page with Bootstrap cards/grid
- `templates/accounts/login.html` - Bootstrap form styling
- `templates/accounts/register.html` - Bootstrap form with validation
- `templates/citizen/dashboard.html` - Bootstrap dashboard layout
- `templates/citizen/services.html` - Bootstrap card grid
- `templates/citizen/apply_form.html` - Bootstrap form with file upload
- `templates/citizen/track.html` - Bootstrap table with status badges
- `templates/officer/dashboard.html` - Bootstrap officer interface
- `templates/admin_panel/dashboard.html` - Bootstrap admin UI
- `templates/mis/dashboard.html` - Bootstrap + Chart.js integration

## Step 3: Verify MySQL Connection
// turbo
```bash
python check_mysql.py
```

## Step 4: Run Migrations
// turbo
```bash
python manage.py makemigrations
python manage.py migrate
```

## Step 5: Test Core Workflows
- Citizen registration and login
- Service application with priority selection
- Officer assignment and review
- Admin dashboard access
- MIS analytics display

## Step 6: Verify RBAC Routing
- `/citizen/*` - Only accessible by role=citizen
- `/officer/*` - Only accessible by role=officer
- `/head/*` - Only accessible by role=head (department_head)
- `/admin-panel/*` - Only accessible by role=admin

## Notes
- All UI should use Bootstrap 5 classes (btn, card, table, badge, etc.)
- Forms should use Bootstrap validation
- Charts should use Chart.js
- No Tailwind CSS should remain
