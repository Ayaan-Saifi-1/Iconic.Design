# Iconic Design

A premium, fully responsive luxury kitchen design and remodeling portfolio website built with Python (Flask) and Bootstrap 5. Crafted with professional-grade glassmorphism aesthetics, fluid scrolling animations, and a powerful dynamic backend.

## Features

- **Professional Luxury Aesthetics:** Deep navy and gold accents with sophisticated glassmorphism layering.
- **Dynamic Scroll Animations:** Integrated AOS (Animate on Scroll) for breathtaking reveals.
- **Responsive Typography:** Features elegant `Playfair Display`, `Cormorant Garamond`, and `Montserrat` pairings that scale perfectly across all devices.
- **Admin Dashboard:** Secure backend to manage kitchen portfolio items, client leads, and system configurations.
- **Dynamic Portfolio Routing:** High-performance database routing for individual project galleries and details.
- **Lead Generation:** Integrated contact modal and email capability via secure environment variables.

## Project Structure

```
Iconic Design/
├── app.py                          # Main Flask Application
├── requirements.txt                # Python dependencies
├── .env.example                    # Template for environment variables
├── .gitignore                      # Security and version control exclusions
├── static/                         # Assets (CSS, client uploads, logos)
└── templates/
    ├── base.html                   # Global layout, glassmorphism UI, logo
    ├── index.html                  # Landing page and service overviews
    ├── all_projects.html           # Full portfolio grid
    ├── project.html                # Dynamic individual project showcase
    ├── admin_login.html            # Secure admin access portal
    └── admin.html                  # Dashboard for lead and project management
```

## Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Ayaan-Saifi-1/Iconic.Design.git
   cd Iconic.Design
   ```

2. **Set up the virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Copy `.env.example` to `.env` and fill in your secure credentials (such as your secret key and email settings).
   ```bash
   cp .env.example .env
   ```

5. **Run the Application:**
   ```bash
   python app.py
   ```

6. **View the site:**
   Open your browser and navigate to `http://localhost:5001`.

## Technology Stack

- **Frontend:** HTML5, CSS3 (Glassmorphism), Bootstrap 5, FontAwesome, AOS Animation Library
- **Backend:** Python 3, Flask Web Framework
- **Database:** SQLite (Production ready via automated schema generation)
- **Deployment Ready:** Configured for DigitalOcean VPS / Gunicorn

## Security & Best Practices
- **Production Ignored Files:** The `.gitignore` protects sensitive data, preventing `.db` files, user-uploaded `/static/uploads`, and `.env` credentials from reaching public version control.
- **Dynamic Database Initialization:** The application detects fresh deployments and automatically scaffolds the `.db` schema without leaking development data.
- **Password Protection:** Admin routes are secured behind session-based authentication.

---
*Built to deliver excellence in culinary spaces.*
