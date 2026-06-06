# Iconic Design — Premium Interior Design Portfolio

A full-stack Flask web application for Iconic Design, a premium interior design studio based in Gurgaon. Features a public-facing portfolio with project showcases, testimonials, and a contact form, plus a complete admin panel for managing content.

## Features

- **Portfolio Showcase** — Paginated project gallery with detailed project pages and image galleries
- **Admin Panel** — Secure login, full CRUD for projects, testimonials, and site settings
- **Contact / Lead Capture** — Contact form saves inquiries to the database and optionally sends email notifications
- **Featured Projects** — Toggle up to 6 projects to appear on the homepage
- **Image Processing** — Auto-converts uploads to optimised WebP; handles smart cropping
- **Performance** — Response compression (`Flask-Compress`), 5-minute page caching, 1-year static asset caching

## Tech Stack

- **Backend:** Python 3.10+, Flask 3.x
- **Database:** SQLite (local dev) — use `DATABASE_PATH` env var to point to a persistent path on your server
- **Images:** Pillow (auto-WebP conversion & cropping)
- **Production:** Gunicorn

## Local Setup

### 1. Prerequisites
- Python 3.10+

### 2. Clone & install

```bash
git clone https://github.com/Ayaan-Saifi-1/Iconic.Design.git
cd Iconic.Design

python -m venv venv
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Environment variables

```bash
cp .env.example .env
# Edit .env and fill in your values
```

### 4. Run locally

```bash
python app.py
```

The app will start on `http://localhost:5001`.  
On first run, the database is auto-created and seeded with sample data (development mode only).

## Production Deployment

### Environment variables to set on your server

| Variable | Description |
|---|---|
| `FLASK_ENV` | Set to `production` |
| `SECRET_KEY` | Long random string for session signing |
| `ADMIN_MASTER_KEY` | Recovery key for admin login |
| `DATABASE_PATH` | Absolute path to a persistent `.db` file on the server |
| `MAIL_USERNAME` | Gmail address for contact form notifications |
| `MAIL_PASSWORD` | Gmail app password |
| `PORT` | Port to bind to (set by most platforms automatically) |

> **Important:** The local `buildcorp.db` database is listed in `.gitignore` and will never be pushed to the repository. Each environment (local / staging / production) maintains its own separate database.

### Start with Gunicorn

```bash
gunicorn app:app --bind 0.0.0.0:8000 --workers 2 --timeout 120
```

Or use the included `Procfile` for Render / Railway / Heroku-compatible platforms.

## Admin Panel

Navigate to `/admin` and log in with the password stored in the database (default: `iconic@admin`).  
Change the password from the admin dashboard after first login.

## Project Structure

```
Iconic.Design/
├── app.py               # Main Flask application
├── requirements.txt     # Python dependencies
├── Procfile             # Production process definition
├── .env.example         # Environment variable template
├── static/
│   └── uploads/         # User-uploaded images (gitignored)
└── templates/           # Jinja2 HTML templates
```
