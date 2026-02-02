# Smart Odisha: e-Governance Service Management System

> **One Citizen, One Digital Platform.**  
> A comprehensive digital interface bridging the gap between the government of Odisha and its citizens through transparency, efficiency, and automation.

![Status](https://img.shields.io/badge/Status-Production%20Ready-success)
![Framework](https://img.shields.io/badge/Stack-Django%20%7C%20Bootstrap-blue)
![Python](https://img.shields.io/badge/Python-3.9%2B-yellow)

---

## 📖 Introduction

The **Smart Odisha** portal is a 3-tier e-governance web application designed to digitize public service delivery. It replaces manual, paper-based workflows with a streamlined, automated online system.

### Key Features
*   **Citizen Dashboard:** Unified view for applications, appointments, and documents.
*   **Intelligent Routing:** Auto-assigns applications to officers to balance workload.
*   **Real-time Tracking:** Granular status updates for every application stage.
*   **Document Locker:** Securely store and reuse personal documents.
*   **SLA Monitoring:** Automated timers to ensure timely service delivery.
*   **Responsive Design:** Fully optimized for Mobile, Tablet, and Desktop.

---

## 🏗 System Modules

1.  **Citizen Module**: Registration, Application Submission, Tracking, Locker, Grievance.
2.  **Officer Module**: Worklist management, Verification, Approval/Rejection.
3.  **MIS Module**: Analytics for Department Heads (Stats, Performance).
4.  **Admin Module**: System Configuration and User Management.

---

## 🚀 Quick Start (Local Development)

### Prerequisites
*   Python 3.9+
*   Git

### Installation

1.  **Clone the Repository**
    ```bash
    git clone <repository_url>
    cd smart-odisha-gov
    ```

2.  **Create Virtual Environment**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Database Setup**
    ```bash
    python manage.py migrate
    python manage.py createsuperuser
    ```

5.  **Run Server**
    ```bash
    python manage.py runserver
    ```
    Access the portal at `http://127.0.0.1:8000/`

---

## 🌐 Deployment (Render)

This project is configured for deployment on **Render.com**.
Refer to `DEPLOYMENT_GUIDE.md` for detailed instructions on setting up the environment variables and build scripts.

---

## 📚 Documentation Included

*   **`PROJECT_DOCUMENTATION.md`**: Full technical & functional overview.
*   **`TESTING_REPORT.md`**: Summary of validation and QA checks.
*   **`SECURITY_DOCUMENTATION.md`**: Details on RBAC, Audit Logs, and compliance.
*   **`DEPLOYMENT_GUIDE.md`**: Step-by-step production deployment manual.

---

## 🛡 Security

The system implements:
*   **Role-Based Access Control (RBAC)**
*   **CSRF & XSS Protection**
*   **Secure Password Hashing (PBKDF2)**
*   **Audit Logging of critical actions**

---

&copy; 2025 Smart Odisha e-Governance Initiative. All Rights Reserved.
