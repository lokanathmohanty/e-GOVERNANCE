# 🔐 Security Documentation: Smart Odisha e-Governance

**Version:** 1.0  
**Classification:** Confidential / Internal Use  

---

## 1. Overview
Security is a foundational pillar of the Smart Odisha platform because it handles sensitive citizen data (Aadhaar, Personal Details). This document outlines the security controls, architectural decisions, and compliance measures implemented in the system.

---

## 2. Authentication & Authorization

### 2.1 Role-Based Access Control (RBAC)
The system enforces strict separation of duties using a custom User model and decorators.
*   **Roles:** `Citizen`, `Officer`, `Department Head`, `Admin`.
*   **Implementation:** Custom decorators (`@role_required`) wrap sensitive views.
    *   *Example:* An URL for `/officer/verify/` will automatically reject a user with `role='citizen'`, returning a 403 Forbidden or redirecting.
*   **Aadhaar Validation:** Unique constraint on Aadhaar numbers ensures identity singularity.

### 2.2 Password Security
*   **Hashing:** All passwords are salted and hashed using **PBKDF2** with SHA-256 (Django default).
*   **Policy:** Enforces complexity (length, mixed case) if configured in settings.

---

## 3. Data Protection

### 3.1 Network Security
*   **HTTPS:** In production (Render), all traffic is forced over HTTPS.
*   **Secure Cookies:**
    *   `SESSION_COOKIE_SECURE = True`
    *   `CSRF_COOKIE_SECURE = True`
    *   `HttpOnly` flags set to prevent XSS access to session tokens.

### 3.2 Cross-Site Request Forgery (CSRF)
*   **Protection:** Django’s CSRF middleware is enabled globally.
*   **Workflow:** All "unsafe" methods (POST, PUT, DELETE) require a valid CSRF token, preventing malicious sites from executing actions on behalf of a logged-in user.

### 3.3 Audit Logging
**"Who did What, When?"**
The `AuditLog` model captures critical modification events:
*   **Fields Logged:** Actor (User), Action (e.g., APPROVED, REJECTED), IP Address, Timestamp, Entity ID.
*   **immutability:** Logs are designed to be append-only for forensic analysis.

---

## 4. Input Validation & Sanitization

*   **Django Forms:** all user input enters via Django Forms/ModelForms which perform strict type checking and validation (e.g., Email format, Regex for Phone).
*   **SQL Injection:** Use of Django ORM abstracts raw SQL queries, neutralizing SQL injection vectors.
*   **XSS (Cross-Site Scripting):** Django Templates auto-escape variables by default (converting `<script>` to `&lt;script&gt;`).

---

## 5. Deployment Security (Render)

*   **Environment Variables:** Secrets (`SECRET_KEY`, `DB_PASSWORD`) are injected at runtime via Environment Variables, never hardcoded in source.
*   **Allowed Hosts:** Restricted to the specific Render domain preventing Host Header attacks.
*   **Static Analysis:** Use of `collectstatic` ensures no executable code is served from static directories.

---

## 6. Incident Response Plan

In case of a suspected breach:
1.  **Isolate:** Suspend the compromised account immediately via Admin Panel.
2.  **Analyze:** Review `AuditLogs` for the specific timeframe.
3.  **Patch:** Deploy fixes via the CI/CD pipeline.
4.  **Notify:** Inform stakeholders.
