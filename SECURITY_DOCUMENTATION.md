# 🔐 Security Documentation

## 1. Overview
Security is a foundational component of the Smart Odisha platform. This document outlines the security measures, protocols, and best practices implemented within the application.

---

## 2. Authentication & Authorization

### 2.1 Role-Based Access Control (RBAC)
We utilize a strict RBAC policy to ensure users can only access resources relevant to their role.
*   **Implementation:** Custom decorators `@role_required(['role_name'])` wrapper around Django views.
*   **Roles:** `citizen`, `officer`, `department_head`, `admin`.
*   **Behavior:** Unauthorized attempts result in immediate redirection and a "Permission Denied" flash message.

### 2.2 Password Security
*   **Hashing:** PBKDF2 algorithm with a SHA256 hash.
*   **Storage:** Passwords are never stored in plain text.
*   **Validation:** Implementation of standard password strength validators (Minimum Length, Common Password, Numeric checks).

---

## 3. Data Protection

### 3.1 Input Validation
*   **Forms:** All user inputs are processed through Django Forms, which provide built-in validation against malicious data types.
*   **Sanitization:** inputs are automatically escaped in templates to prevent Cross-Site Scripting (XSS).

### 3.2 CSRF Protection
*   **Mechanism:** Cross-Site Request Forgery (CSRF) tokens are required for every state-changing request (POST, PUT, DELETE).
*   **Enforcement:** Django middleware `CsrfViewMiddleware` is active globally.

### 3.3 SQL Injection
*   **Prevention:** The project strictly uses Django ORM querysets (e.g., `Application.objects.filter()`) instead of raw SQL queries, neutralizing SQL injection vectors.

---

## 4. Audit & Monitoring

### 4.1 Audit Logs
A dedicated `AuditLog` model tracks sensitive system actions.
*   **Tracked Events:** Login, Registration, Application Submission, Approval/Rejection, Grievance Filing.
*   **Data Points:** User ID, Action Type, Timestamp, IP Address.
*   **Immutability:** The Audit Log model is designed to be append-only in the application logic.

### 4.2 Login History
*   To detect account compromise, the system maintains a history of user logins, recording the IP and User-Agent string.

---

## 5. Deployment Security Checklist

Before going live, the following settings MUST be enforced in production (`settings.py`):

- [ ] **DEBUG = False**: Prevents leakage of stack traces and configuration options.
- [ ] **ALLOWED_HOSTS**: Restrict to specific domain names.
- [ ] **SECURE_SSL_REDIRECT = True**: Force HTTPS connections.
- [ ] **SESSION_COOKIE_SECURE = True**: Cookies only sent over HTTPS.
- [ ] **CSRF_COOKIE_SECURE = True**: CSRF tokens only sent over HTTPS.
- [ ] **Secret Key Rotation**: Use a unique, unpredictable secret key loaded from environment variables.

---

## 6. Incident Response Plan

In the event of a security breach:
1.  **Isolate:** Take the instance offline or enable "Maintenance Mode".
2.  **Investigate:** Review `AuditLog` and `LoginHistory` tables.
3.  **Patch:** Apply necessary code fixes.
4.  **Notify:** Inform affected users (if personal data was compromised) in accordance with government regulations.

---
**Confidentiality Level:** Internal / Public (Safe for technical review)
