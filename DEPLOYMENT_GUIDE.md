# Deploying Your Django Project: Step-by-Step Guide

This guide will help you deploy your **e-Governance Service Management System** to a live server. We will look at a general "Production Ready" workflow, which is applicable to most platforms like **Render**, **Railway**, **PythonAnywhere**, or a **VPS** (DigitalOcean/AWS).

---

## 🚀 Phase 1: Preparation (Already Done)
Your project is already well-configured for deployment!
✅ **`requirements.txt`**: Exists and includes `gunicorn` and `whitenoise`.
✅ **`settings.py`**: Configured to load variables from `.env` and use `whitenoise` for static files.
✅ **WSGI**: Exists at `egovernance/wsgi.py`.

---

## 🛠 Phase 2: Configuration for Production

### 1. Create a `.env` file on the Server
On your live server configuration dashboard (or `.env` file), you **MUST** set these values. Do not check this file into Git.

```ini
# Security
DEBUG=False
SECRET_KEY=your-super-long-secret-key-here-that-no-one-can-guess
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database (PostgreSQL is recommended for Prod, but MySQL works too)
DB_NAME=egov_prod_db
DB_USER=egov_user
DB_PASSWORD=your_secure_db_password
DB_HOST=db.yourserver.com
DB_PORT=5432  # Use 5432 for Postgres, 3306 for MySQL
```

### 2. Update `settings.py` (Optional Check)
Make sure your Database setting automatically handles PostgreSQL if you switch engines. Currently, it is hardcoded for MySQL. For a generic cloud deployment (which often uses Postgres), usually, you replace the `DATABASES` block with `dj_database_url` (optional, but standard).

*Current:`mysqlclient` is in your `requirements.txt`* -> **Ensure your production server has MySQL installed.**

---

## ☁️ Phase 3: Choose a Deployment Platform

### Option A: Render (Easiest & Free Tier)
1.  **Push your code to GitHub.**
2.  **Sign up** at [render.com](https://render.com).
3.  Click **"New +"** → **"Web Service"**.
4.  Connect your GitHub repository.
5.  **Settings:**
    *   **Runtime:** Python 3
    *   **Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
    *   **Start Command:** `gunicorn egovernance.wsgi:application`
6.  **Environment Variables:** Add the keys from Phase 2 (DB_NAME, etc.).

### Option B: PythonAnywhere (Great for Django)
1.  **Sign up** at [pythonanywhere.com](https://www.pythonanywhere.com/).
2.  **Upload Code:** Use the "Bash" console to `git clone` your repo.
3.  **Virtual Env:**
    ```bash
    mkvirtualenv --python=/usr/bin/python3.10 my-project-env
    pip install -r requirements.txt
    ```
4.  **Static Files:** Go to the "Web" tab and map `/static/` to your project's `staticfiles` folder path.
5.  **WSGI Config:** Edit the WSGI configuration file (link in "Web" tab) to point to your project folder and settings.

---

## 📦 Phase 4: Final Steps on Server

Once your code is on the server, functionality depends on these commands running successfully:

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Collect Static Files:**
    (This moves all CSS/JS to one folder for the server to find)
    ```bash
    python manage.py collectstatic
    ```

3.  **Run Migrations:**
    (This builds your database tables on the live DB)
    ```bash
    python manage.py migrate
    ```

4.  **Create Superuser:**
    (To access the Admin panel live)
    ```bash
    python manage.py createsuperuser
    ```

---

## ⚠️ Important Checks
*   **Debug Mode:** Ensure `DEBUG = False` in production.
*   **Allowed Hosts:** The domain name (e.g., `myapp.onrender.com`) must be in `ALLOWED_HOSTS`.
*   **Database:** If you switch from local MySQL to a cloud Postgres, you usually just need to `pip install psycopg2-binary` and update the `DATABASES` setting.

**You are ready to go live!** 🚀
