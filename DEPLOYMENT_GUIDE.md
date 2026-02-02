# 🚀 Deployment Guide: Smart Odisha on Render

This guide outlines the steps to deploy the **e-Governance Service Management System** to production using **Render.com**.

---

## 1. Prerequisites
*   A **Render** account (https://render.com).
*   The project code pushed to a **GitHub** repository.
*   Production-ready `build.sh` script (included in root).

---

## 2. Configuration Files Verification
Ensure these files are present in your repository root:

1.  **`requirements.txt`**: Must include `gunicorn`, `psycopg2-binary`, `dj-database-url`, `whitenoise`.
2.  **`build.sh`**:
    ```bash
    #!/usr/bin/env bash
    set -o errexit
    pip install -r requirements.txt
    python manage.py collectstatic --no-input
    python manage.py migrate
    ```
3.  **`Procfile`** (Optional but recommended):
    ```
    web: gunicorn egovernance.wsgi
    ```
4.  **`runtime.txt`** (Optional): Specifies Python version (e.g., `python-3.9.18`).

---

## 3. Render Setup Steps

### Step 1: Create Web Service
1.  Log in to Render Dashboard.
2.  Click **New +** -> **Web Service**.
3.  Connect your GitHub repository.

### Step 2: Configure Environment
*   **Name:** `smart-odisha-gov` (or your choice)
*   **Region:** Singapore (or nearest to user base)
*   **Branch:** `main`
*   **Runtime:** Python 3
*   **Build Command:** `./build.sh`
*   **Start Command:** `gunicorn egovernance.wsgi:application`

### Step 3: Environment Variables
Add the following key-value pairs in the **Environment** tab:

| Key | Value | Description |
| :--- | :--- | :--- |
| `PYTHON_VERSION` | `3.9.18` | Ensure compatibility |
| `SECRET_KEY` | `(Generate a long random string)` | Django Security Key |
| `DEBUG` | `False` | **CRITICAL for Production** |
| `ALLOWED_HOSTS` | `.onrender.com` | Allow Render domains |
| `DATABASE_URL` | `(Internal connection string)` | *See Step 4 below* |

### Step 4: Add Database (PostgreSQL)
1.  Go to Render Dashboard -> **New +** -> **PostgreSQL**.
2.  Name it `smart-odisha-db`.
3.  Once created, copy the **Internal Database URL**.
4.  Go back to your Web Service -> **Environment**.
5.  Add `DATABASE_URL` and paste the connection string.

---

## 4. Post-Deployment Verification

1.  **Check Logs:** Ensure the build finishes with "Build successful" and "Deploying...".
2.  **Create Superuser:**
    *   In Render Dashboard, go to **Shell**.
    *   Run: `python manage.py createsuperuser`
3.  **Access Site:** Visit your `https://<your-app>.onrender.com` URL.
4.  **Verify Static Files:** Check if CSS/Images load correctly (confirms WhiteNoise is working).

---

## 5. Troubleshooting Common Issues

*   **Error: `ModuleNotFoundError`**: Check `requirements.txt`.
*   **Static Files 404**: Ensure `Check logic in settings.py` has `STATICFILES_STORAGE` set to WhiteNoise.
*   **Database Error**: Verify `DATABASE_URL` is correct and the database service is "Available".

---

## 6. Maintenance
*   **Logs:** Monitor "Logs" tab in Render for runtime errors.
*   **Updates:** Pushing code to `main` branch automatically triggers a redeploy.
