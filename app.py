"""
Iconic Design Portfolio Backend
==========================================
This is the main Flask application for the Iconic Design interior design portfolio website.
Database: PostgreSQL via Supabase (psycopg2)
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

import psycopg2
import psycopg2.extras
import math
import uuid
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from werkzeug.utils import secure_filename
from PIL import Image


def process_and_save_image(file_obj, upload_folder, max_dim=2560):
    if not file_obj or not file_obj.filename:
        return None

    filename = secure_filename(file_obj.filename)
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    unique_filename = f"{uuid.uuid4().hex}"

    if ext == 'svg':
        final_filename = f"{unique_filename}.svg"
        save_path = os.path.join(upload_folder, final_filename)
        file_obj.save(save_path)
        return f"/static/uploads/{final_filename}"

    try:
        img = Image.open(file_obj)
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')

        width, height = img.size
        if width > max_dim or height > max_dim:
            if width > height:
                new_width = max_dim
                new_height = int((max_dim / width) * height)
            else:
                new_height = max_dim
                new_width = int((max_dim / height) * width)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        final_filename = f"{unique_filename}.webp"
        save_path = os.path.join(upload_folder, final_filename)
        img.save(save_path, 'WEBP', quality=90)
        return f"/static/uploads/{final_filename}"
    except Exception as e:
        print(f"Image processing failed: {e}")
        save_path = os.path.join(upload_folder, filename)
        file_obj.seek(0)
        file_obj.save(save_path)
        return f"/static/uploads/{filename}"


def process_and_crop_image(file_obj, upload_folder, aspect_ratio=(4, 5), target_width=800):
    if not file_obj or not file_obj.filename:
        return None

    filename = secure_filename(file_obj.filename)
    unique_filename = f"{uuid.uuid4().hex}"

    try:
        img = Image.open(file_obj)
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')

        width, height = img.size
        target_aspect = aspect_ratio[0] / aspect_ratio[1]
        img_aspect = width / height

        if img_aspect > target_aspect:
            # Image is too wide -> crop left and right
            new_width = int(height * target_aspect)
            offset = (width - new_width) // 2
            img = img.crop((offset, 0, offset + new_width, height))
        else:
            # Image is too tall -> crop top and bottom (bias vertical crop slightly towards top)
            new_height = int(width / target_aspect)
            offset = int((height - new_height) * 0.35)
            img = img.crop((0, offset, width, offset + new_height))

        target_height = int(target_width / target_aspect)
        img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)

        final_filename = f"{unique_filename}.webp"
        save_path = os.path.join(upload_folder, final_filename)
        img.save(save_path, 'WEBP', quality=90)
        return f"/static/uploads/{final_filename}"
    except Exception as e:
        print(f"Image cropping and processing failed: {e}")
        save_path = os.path.join(upload_folder, filename)
        file_obj.seek(0)
        file_obj.save(save_path)
        return f"/static/uploads/{filename}"


from flask_compress import Compress
from flask_caching import Cache

app = Flask(__name__)
# SECRET KEY: In production, set the SECRET_KEY environment variable on your hosting platform.
# Never commit a real secret key to a public repository.
app.secret_key = os.environ.get('SECRET_KEY', 'iconic_design_local_dev_key_change_in_production')

# Initialize Compression
compress = Compress()
compress.init_app(app)

# Initialize Caching
cache = Cache(config={'CACHE_TYPE': 'SimpleCache', 'CACHE_DEFAULT_TIMEOUT': 300})
cache.init_app(app)

# --- CONFIGURATION ---
PROJECTS_PER_PAGE = 9
# DATABASE_URL env var: set this to your Supabase PostgreSQL connection string in production.
DATABASE_URL = os.environ.get('DATABASE_URL')
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def get_db_connection():
    """Returns a psycopg2 connection using RealDictCursor so rows behave like dicts."""
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=psycopg2.extras.RealDictCursor)
    return conn


def _column_exists(cursor, table, column):
    """Check if a column already exists in a table (PostgreSQL-safe ALTER TABLE guard)."""
    cursor.execute(
        """
        SELECT 1 FROM information_schema.columns
        WHERE table_name = %s AND column_name = %s
        """,
        (table, column)
    )
    return cursor.fetchone() is not None


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create projects table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            location TEXT,
            date TEXT,
            description TEXT,
            status TEXT,
            budget TEXT,
            team_size TEXT,
            duration TEXT,
            cover_image TEXT,
            full_details TEXT
        )
    ''')

    # Add extra columns if they don't exist yet (safe ALTER TABLE for PostgreSQL)
    extra_columns = [
        ('scope_of_work', 'TEXT'),
        ('achievements', 'TEXT'),
        ('extended_description', 'TEXT'),
        ('scope_heading', 'TEXT'),
        ('achievements_heading', 'TEXT'),
        ('achievements_subheading', 'TEXT'),
        ('is_featured', 'INTEGER DEFAULT 0'),
    ]
    for col_name, col_type in extra_columns:
        if not _column_exists(cursor, 'projects', col_name):
            cursor.execute(f'ALTER TABLE projects ADD COLUMN {col_name} {col_type}')

    # Migrate any missing data for existing rows to default text
    default_scope = "Comprehensive structural design and engineering\nComplete construction execution with modern equipment\nQuality assurance and compliance testing\nSafety management and environmental protection\nProject completion within budget and timeline\nPost-construction support and maintenance"
    default_achievements = "ISO 9001:2015 - Quality Management System\nLEED Green Building - Environmental Excellence\nSafety Excellence Award - Accident-Free Record\nOn-Time Delivery - Project Management Excellence"
    default_extended = "This landmark project exemplifies our commitment to excellence, innovation, and sustainable development. Every aspect of the construction was carefully planned and executed to meet the highest industry standards while ensuring minimal environmental impact."

    cursor.execute('UPDATE projects SET scope_of_work = %s WHERE scope_of_work IS NULL', (default_scope,))
    cursor.execute('UPDATE projects SET achievements = %s WHERE achievements IS NULL', (default_achievements,))
    cursor.execute('UPDATE projects SET extended_description = %s WHERE extended_description IS NULL', (default_extended,))
    cursor.execute("UPDATE projects SET scope_heading = %s WHERE scope_heading IS NULL", ('Scope of Work',))
    cursor.execute("UPDATE projects SET achievements_heading = %s WHERE achievements_heading IS NULL", ('Achievements & Certifications',))
    cursor.execute("UPDATE projects SET achievements_subheading = %s WHERE achievements_subheading IS NULL", ('This project received recognition for:',))

    # Ensure at least some projects are featured initially
    cursor.execute('SELECT COUNT(*) FROM projects WHERE is_featured = 1')
    featured_count = cursor.fetchone()['count']
    if featured_count == 0:
        cursor.execute('UPDATE projects SET is_featured = 1 WHERE id IN (SELECT id FROM projects ORDER BY date DESC LIMIT 3)')

    # Create project_images table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS project_images (
            id SERIAL PRIMARY KEY,
            project_id INTEGER,
            image_path TEXT,
            FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
        )
    ''')

    # Create testimonials table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS testimonials (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            text TEXT NOT NULL,
            stars INTEGER DEFAULT 5,
            sort_order INTEGER DEFAULT 0,
            is_active INTEGER DEFAULT 1
        )
    ''')

    # Seed testimonials if empty
    cursor.execute('SELECT COUNT(*) FROM testimonials')
    testimonial_count = cursor.fetchone()['count']
    if testimonial_count == 0:
        seed_testimonials = [
            ('Rajesh Kumar', 'Homeowner, Mumbai', 'Iconic Design exceeded our expectations. Our newly designed living room is the absolute centerpiece of our home!', 5, 1),
            ('Priya Sharma', 'Homeowner & Interior Enthusiast', 'Their attention to detail and spatial planning makes living in our home an absolute joy every single day.', 5, 2),
            ('Vikram Patel', 'Architectural Consultant', 'Exceptional material quality and transparent communication. The transformation was seamless and utterly perfect.', 5, 3),
        ]
        cursor.executemany(
            'INSERT INTO testimonials (name, role, text, stars, sort_order) VALUES (%s, %s, %s, %s, %s)',
            seed_testimonials
        )

    # Create settings table for dynamic admin password and site config
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    ''')
    cursor.execute(
        "INSERT INTO settings (key, value) VALUES (%s, %s) ON CONFLICT (key) DO NOTHING",
        ('admin_password', 'iconic@admin')
    )

    # Seed homepage stats & founder settings
    default_stats = [
        ('stat1_value', '100+'), ('stat1_label', 'Projects Delivered'),
        ('stat2_value', '25'),   ('stat2_label', 'Years of Mastery'),
        ('stat3_value', '50+'),  ('stat3_label', 'Expert Designers'),
        ('stat4_value', '99%'),  ('stat4_label', 'Client Satisfaction'),
        ('founder_name', 'Shakir Ali'),
        ('founder_title', 'Founder'),
        ('founder_phone', '+91 98116 85628'),
        ('founder_email', 'shakirali1203@gmail.com'),
        ('founder_location', 'Sector 56, Gurgaon'),
        ('founder_image', '/static/uploads/shakir_ali.png'),
        ('hero_badge', "India's Premier Interior Designers"),
        ('hero_title', 'Crafting Iconic Interiors'),
        ('hero_desc', 'With over 25 years of experience, Iconic Design delivers premium interior design, luxury decoration, and bespoke residential environments tailored to your lifestyle.'),
        ('about_subtitle', 'Your Trusted Design Partner'),
        ('about_desc1', 'iconic.design, founded by visionary designer Shakir Ali, stands as a beacon of excellence in the premium interior design and luxury decoration industry. Based in Sector 56, Gurgaon, we specialize in delivering world-class residential transformations, high-end commercial spaces, and custom-tailored environments that elevate your lifestyle.'),
        ('about_desc2', "Under Shakir Ali's leadership, our team of expert decorators and craftsmen combine aesthetic innovation, spatial ergonomics, and premium material curation. We are committed to turning your residential and commercial visions into reality with immaculate execution and transparent service."),
        ('about_bullet1', 'Bespoke Furniture & Material Curation'),
        ('about_bullet2', 'End-to-End Space Planning & Execution'),
        ('about_bullet3', 'Immaculate Craftsmanship & Finishing'),
    ]
    for key, value in default_stats:
        cursor.execute(
            "INSERT INTO settings (key, value) VALUES (%s, %s) ON CONFLICT (key) DO NOTHING",
            (key, value)
        )

    # Create leads table for contact form inquiries
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            project_type TEXT,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # --- Performance Indexes ---
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_projects_date ON projects(date DESC)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_projects_status ON projects(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_leads_created ON leads(created_at DESC)')

    # Check if empty, then seed with dummy data only in development
    cursor.execute('SELECT COUNT(*) FROM projects')
    project_count = cursor.fetchone()['count']
    if project_count == 0:
        if os.environ.get('FLASK_ENV') != 'production':
            print("Development environment detected. Database is empty. Seeding with initial data...")
            seed_db(cursor)
        else:
            print("Production environment detected. Database initialized as empty.")

    conn.commit()
    conn.close()


def seed_db(cursor):
    project_types = ["Modern Living Room", "Luxury Villa Interiors", "Bespoke Bedroom Suite", "Contemporary Dining Area", "Custom Interior Styling"]
    locations = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Pune"]
    descriptions = ["A stunning {type} designed with premium materials, spatial harmony, and seamless aesthetics."]

    default_scope = "Comprehensive space planning and layout\nBespoke furniture selection and sourcing\nCustom lighting design and ambiance\nPremium material finishes and texturing\nArt curation and styling\nComplete installation and staging"
    default_achievements = "Premium Quality Materials\nSpatial Excellence\nBespoke Furniture Solutions\nImmaculate Styling"
    default_extended = "This iconic space was crafted to merge luxury with breathtaking design. Every element, from the bespoke furniture to the lighting, was carefully curated to create a truly magnificent environment."

    for i in range(1, 101):
        ptype = project_types[i % len(project_types)]
        loc = locations[i % len(locations)]
        days_ago = (i * 11) % 1095
        pdate = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        cover_image = f"/static/uploads/project-{(i % 12) + 1}.svg"

        cursor.execute('''
            INSERT INTO projects (title, location, date, description, status, budget, team_size, duration, cover_image, scope_of_work, achievements, extended_description, scope_heading, achievements_heading, achievements_subheading)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        ''', (
            f"{ptype} - Phase {(i % 5) + 1}",
            loc,
            pdate,
            descriptions[0].format(type=ptype),
            ["Completed", "In Progress", "Planning"][i % 3],
            f"₹1{(i % 50 + 1)} Crores",
            f"{30 + (i % 50)} Professionals",
            f"{6 + (i % 20)} Months",
            cover_image,
            default_scope,
            default_achievements,
            default_extended,
            'Scope of Work',
            'Achievements & Certifications',
            'This project received recognition for:'
        ))
        project_id = cursor.fetchone()['id']

        # Add gallery images (including cover image as first)
        cursor.execute('INSERT INTO project_images (project_id, image_path) VALUES (%s, %s)', (project_id, cover_image))
        for j in range(5):
            cursor.execute(
                'INSERT INTO project_images (project_id, image_path) VALUES (%s, %s)',
                (project_id, f"/static/uploads/gallery-{(j % 4) + 1}.svg")
            )


init_db()


@app.context_processor
def inject_settings():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT key, value FROM settings')
        all_settings = cursor.fetchall()
        conn.close()
        settings_dict = {row['key']: row['value'] for row in all_settings}
    except Exception:
        settings_dict = {}
    return dict(site_settings=settings_dict)


# --- ROUTES ---

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get total count of all projects for the "View All X Projects" button
    cursor.execute('SELECT COUNT(*) FROM projects')
    total_projects = cursor.fetchone()['count']

    # Fetch all featured projects for the homepage
    cursor.execute('SELECT * FROM projects WHERE is_featured = 1 ORDER BY date DESC')
    projects = cursor.fetchall()

    cursor.execute('SELECT * FROM testimonials WHERE is_active = 1 ORDER BY sort_order ASC')
    testimonials = cursor.fetchall()

    # Load stats from settings
    cursor.execute('SELECT key, value FROM settings')
    all_settings = cursor.fetchall()
    settings_dict = {row['key']: row['value'] for row in all_settings}

    class Stats:
        stat1_value = settings_dict.get('stat1_value', '100+')
        stat1_label = settings_dict.get('stat1_label', 'Projects Delivered')
        stat2_value = settings_dict.get('stat2_value', '25')
        stat2_label = settings_dict.get('stat2_label', 'Years of Mastery')
        stat3_value = settings_dict.get('stat3_value', '50+')
        stat3_label = settings_dict.get('stat3_label', 'Expert Designers')
        stat4_value = settings_dict.get('stat4_value', '99%')
        stat4_label = settings_dict.get('stat4_label', 'Client Satisfaction')

    conn.close()

    return render_template(
        'index.html',
        projects=projects,
        total_projects=total_projects,
        testimonials=testimonials,
        stats=Stats(),
    )


@app.route('/projects')
def all_projects():
    page = request.args.get('page', 1, type=int)
    if page < 1: page = 1

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM projects')
    total_projects = cursor.fetchone()['count']
    total_pages = math.ceil(total_projects / PROJECTS_PER_PAGE) if total_projects > 0 else 1

    if page > total_pages: page = total_pages

    offset = (page - 1) * PROJECTS_PER_PAGE

    cursor.execute(
        'SELECT * FROM projects ORDER BY date DESC LIMIT %s OFFSET %s',
        (PROJECTS_PER_PAGE, offset)
    )
    projects = cursor.fetchall()

    conn.close()

    return render_template(
        'all_projects.html',
        projects=projects,
        current_page=page,
        total_pages=total_pages,
        total_projects=total_projects
    )


@app.route('/project/<int:project_id>')
def project_detail(project_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM projects WHERE id = %s', (project_id,))
    project = cursor.fetchone()

    if project is None:
        conn.close()
        return "Project not found", 404

    cursor.execute('SELECT * FROM project_images WHERE project_id = %s', (project_id,))
    gallery_images = cursor.fetchall()

    cursor.execute(
        'SELECT * FROM projects WHERE location = %s AND id != %s LIMIT 3',
        (project['location'], project_id)
    )
    related_projects = cursor.fetchall()

    conn.close()

    return render_template(
        'project.html',
        project=project,
        project_id=project_id,
        related_projects=related_projects,
        gallery_images=gallery_images
    )


# --- ADMIN ROUTES ---

from flask import session


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password')

        # Recovery master key — set ADMIN_MASTER_KEY in your server env vars.
        MASTER_KEY = os.environ.get('ADMIN_MASTER_KEY', '')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = 'admin_password'")
        row = cursor.fetchone()
        conn.close()

        # Allow login if password matches the database OR the master key
        if password == MASTER_KEY or (row and password == row['value']):
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid password', 'error')
    return render_template('admin_login.html')


@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))


@app.route('/admin/password', methods=['POST'])
def admin_password():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    new_password = request.form.get('new_password')
    if new_password and len(new_password) >= 6:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE settings SET value = %s WHERE key = 'admin_password'", (new_password,))
        conn.commit()
        conn.close()
        flash('Admin password successfully updated!', 'success')
    else:
        flash('Password must be at least 6 characters.', 'error')

    return redirect(url_for('admin_dashboard'))


@app.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        # Handle Project Creation
        title = request.form.get('title')
        location = request.form.get('location')
        date = request.form.get('date')
        status = request.form.get('status')
        budget = request.form.get('budget')
        team_size = request.form.get('team_size')
        duration = request.form.get('duration')
        description = request.form.get('description')
        scope_of_work = request.form.get('scope_of_work')
        achievements = request.form.get('achievements')
        extended_description = request.form.get('extended_description')
        scope_heading = request.form.get('scope_heading') or 'Scope of Work'
        achievements_heading = request.form.get('achievements_heading') or 'Achievements & Certifications'
        achievements_subheading = request.form.get('achievements_subheading') or 'This project received recognition for:'

        # Handle Cover Image Upload
        cover_image_file = request.files.get('cover_image')
        cover_image_path = "/static/uploads/project-1.svg"  # Default fallback
        if cover_image_file and cover_image_file.filename:
            processed_path = process_and_save_image(cover_image_file, app.config['UPLOAD_FOLDER'])
            if processed_path:
                cover_image_path = processed_path

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO projects (title, location, date, description, status, budget, team_size, duration, cover_image, scope_of_work, achievements, extended_description, scope_heading, achievements_heading, achievements_subheading)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        ''', (title, location, date, description, status, budget, team_size, duration, cover_image_path, scope_of_work, achievements, extended_description, scope_heading, achievements_heading, achievements_subheading))
        project_id = cursor.fetchone()['id']

        # Add cover image to gallery by default
        cursor.execute('INSERT INTO project_images (project_id, image_path) VALUES (%s, %s)', (project_id, cover_image_path))

        # Handle Gallery Images Upload
        gallery_files = request.files.getlist('gallery_images')
        for file in gallery_files:
            if file and file.filename:
                processed_path = process_and_save_image(file, app.config['UPLOAD_FOLDER'])
                if processed_path:
                    cursor.execute('INSERT INTO project_images (project_id, image_path) VALUES (%s, %s)', (project_id, processed_path))

        conn.commit()
        conn.close()
        flash('Project successfully added!', 'success')
        return redirect(url_for('admin_dashboard'))

    # Pagination logic for Admin panel
    page = request.args.get('page', 1, type=int)
    if page < 1: page = 1
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM projects')
    total_projects = cursor.fetchone()['count']
    total_pages = math.ceil(total_projects / PROJECTS_PER_PAGE) if total_projects > 0 else 1
    if page > total_pages: page = total_pages
    offset = (page - 1) * PROJECTS_PER_PAGE

    cursor.execute('SELECT id, title, date, is_featured FROM projects ORDER BY date DESC LIMIT %s OFFSET %s', (PROJECTS_PER_PAGE, offset))
    projects = cursor.fetchall()
    conn.close()

    return render_template('admin.html', projects=projects, current_page=page, total_pages=total_pages)


@app.route('/admin/toggle_feature/<int:project_id>', methods=['POST'])
def admin_toggle_feature(project_id):
    if not session.get('admin_logged_in'):
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT is_featured FROM projects WHERE id = %s', (project_id,))
    project = cursor.fetchone()
    if project:
        current_status = project['is_featured']

        # If turning ON, check the 6-project limit
        if current_status == 0:
            cursor.execute('SELECT COUNT(*) FROM projects WHERE is_featured = 1')
            featured_count = cursor.fetchone()['count']
            if featured_count >= 6:
                conn.close()
                return jsonify({'success': False, 'limit_reached': True, 'error': 'You already have 6 featured projects. Please unfeature one before adding another.'})

        new_status = 1 if current_status == 0 else 0
        cursor.execute('UPDATE projects SET is_featured = %s WHERE id = %s', (new_status, project_id))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'is_featured': new_status})

    conn.close()
    return jsonify({'success': False, 'error': 'Project not found'}), 404


@app.route('/admin/leads')
def admin_leads():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    page = request.args.get('page', 1, type=int)
    if page < 1: page = 1

    LEADS_PER_PAGE = 10
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM leads')
    total_leads = cursor.fetchone()['count']
    total_pages = math.ceil(total_leads / LEADS_PER_PAGE) if total_leads > 0 else 1

    if page > total_pages: page = total_pages
    offset = (page - 1) * LEADS_PER_PAGE

    cursor.execute('SELECT * FROM leads ORDER BY created_at DESC LIMIT %s OFFSET %s', (LEADS_PER_PAGE, offset))
    leads = cursor.fetchall()
    conn.close()

    return render_template('admin_leads.html', leads=leads, current_page=page, total_pages=total_pages, total_leads=total_leads)


@app.route('/admin/leads/delete/<int:lead_id>', methods=['POST'])
def admin_delete_lead(lead_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM leads WHERE id = %s', (lead_id,))
    conn.commit()
    conn.close()
    flash('Inquiry successfully deleted.', 'success')
    return redirect(url_for('admin_leads'))


@app.route('/admin/delete/<int:project_id>', methods=['POST'])
def admin_delete_project(project_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM project_images WHERE project_id = %s', (project_id,))
    cursor.execute('DELETE FROM projects WHERE id = %s', (project_id,))
    conn.commit()
    conn.close()

    flash('Project deleted successfully.', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/edit/<int:project_id>', methods=['GET', 'POST'])
def admin_edit_project(project_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        title = request.form.get('title')
        location = request.form.get('location')
        date = request.form.get('date')
        status = request.form.get('status')
        budget = request.form.get('budget')
        team_size = request.form.get('team_size')
        duration = request.form.get('duration')
        description = request.form.get('description')
        scope_of_work = request.form.get('scope_of_work')
        achievements = request.form.get('achievements')
        extended_description = request.form.get('extended_description')
        scope_heading = request.form.get('scope_heading') or 'Scope of Work'
        achievements_heading = request.form.get('achievements_heading') or 'Achievements & Certifications'
        achievements_subheading = request.form.get('achievements_subheading') or 'This project received recognition for:'

        # Optional new cover image
        cover_image_file = request.files.get('cover_image')

        if cover_image_file and cover_image_file.filename:
            processed_path = process_and_save_image(cover_image_file, app.config['UPLOAD_FOLDER'])
            if processed_path:
                cover_image_path = processed_path
                cursor.execute('''
                    UPDATE projects
                    SET title=%s, location=%s, date=%s, description=%s, status=%s, budget=%s, team_size=%s, duration=%s, cover_image=%s, scope_of_work=%s, achievements=%s, extended_description=%s, scope_heading=%s, achievements_heading=%s, achievements_subheading=%s
                    WHERE id=%s
                ''', (title, location, date, description, status, budget, team_size, duration, cover_image_path, scope_of_work, achievements, extended_description, scope_heading, achievements_heading, achievements_subheading, project_id))
        else:
            cursor.execute('''
                UPDATE projects
                SET title=%s, location=%s, date=%s, description=%s, status=%s, budget=%s, team_size=%s, duration=%s, scope_of_work=%s, achievements=%s, extended_description=%s, scope_heading=%s, achievements_heading=%s, achievements_subheading=%s
                WHERE id=%s
            ''', (title, location, date, description, status, budget, team_size, duration, scope_of_work, achievements, extended_description, scope_heading, achievements_heading, achievements_subheading, project_id))

        # Handle optional Gallery Images Upload
        gallery_files = request.files.getlist('gallery_images')
        for file in gallery_files:
            if file and file.filename:
                processed_path = process_and_save_image(file, app.config['UPLOAD_FOLDER'])
                if processed_path:
                    cursor.execute('INSERT INTO project_images (project_id, image_path) VALUES (%s, %s)', (project_id, processed_path))

        conn.commit()
        conn.close()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    cursor.execute('SELECT * FROM projects WHERE id = %s', (project_id,))
    project = cursor.fetchone()
    if project is None:
        conn.close()
        return "Project not found", 404

    cursor.execute('SELECT * FROM project_images WHERE project_id = %s', (project_id,))
    gallery_images = cursor.fetchall()
    conn.close()

    return render_template('admin_edit.html', project=project, gallery_images=gallery_images)


@app.route('/admin/delete_image/<int:image_id>', methods=['POST'])
def admin_delete_image(image_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM project_images WHERE id = %s', (image_id,))
    image = cursor.fetchone()
    if image:
        project_id = image['project_id']
        cursor.execute('DELETE FROM project_images WHERE id = %s', (image_id,))
        conn.commit()

        # Try to delete from filesystem
        try:
            if image['image_path'].startswith('/static/'):
                filepath = image['image_path'].lstrip('/')
                if os.path.exists(filepath):
                    os.remove(filepath)
        except Exception as e:
            print(f"Failed to delete image file: {e}")

        flash('Gallery image deleted successfully.', 'success')
        conn.close()
        return redirect(url_for('admin_edit_project', project_id=project_id))

    conn.close()
    return redirect(url_for('admin_dashboard'))


@app.route('/api/contact', methods=['POST'])
def contact_form():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    project_type = request.form.get('project_type')
    message_text = request.form.get('message')

    # Save to database
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO leads (name, email, phone, project_type, message) VALUES (%s, %s, %s, %s, %s)',
            (name, email, phone, project_type, message_text)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Database Error: {e}")
        flash('An error occurred. Please try again.', 'error')
        return redirect(url_for('index', _anchor='contact'))

    # Send email
    try:
        sender_email = os.environ.get('MAIL_USERNAME')
        sender_password = os.environ.get('MAIL_PASSWORD')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = 'founder_email'")
        row = cursor.fetchone()
        conn.close()
        receiver_email = row['value'] if row else 'shakirali1203@gmail.com'

        if sender_email and sender_password:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = f"New Inquiry: {project_type} from {name}"

            body = f"""
New Iconic Design Inquiry Received!

Name: {name}
Email: {email}
Phone: {phone}
Project Type: {project_type}

Message:
{message_text}
"""
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()
        else:
            print("WARNING: MAIL_USERNAME or MAIL_PASSWORD not set. Email not sent, but lead saved.")

        flash('Your inquiry has been sent successfully!', 'success')
    except Exception as e:
        print(f"Email Error: {e}")
        flash('Your inquiry was received, but email notification failed.', 'success')

    return redirect(url_for('index', _anchor='contact'))


# --- ADMIN TESTIMONIALS ---

@app.route('/admin/testimonials', methods=['GET', 'POST'])
def admin_testimonials():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        role = request.form.get('role', '').strip()
        text = request.form.get('text', '').strip()
        stars = int(request.form.get('stars', 5))
        is_active = 1 if request.form.get('is_active') else 0

        if name and role and text:
            cursor.execute('SELECT COALESCE(MAX(sort_order), 0) FROM testimonials')
            max_order = cursor.fetchone()['coalesce']
            cursor.execute(
                'INSERT INTO testimonials (name, role, text, stars, sort_order, is_active) VALUES (%s, %s, %s, %s, %s, %s)',
                (name, role, text, stars, max_order + 1, is_active)
            )
            conn.commit()
            conn.close()
            flash('Testimonial added successfully!', 'success')
        else:
            flash('Name, role, and testimonial text are required.', 'error')
        return redirect(url_for('admin_testimonials'))

    cursor.execute('SELECT * FROM testimonials ORDER BY sort_order ASC')
    testimonials = cursor.fetchall()
    conn.close()
    return render_template('admin_testimonials.html', testimonials=testimonials)


@app.route('/admin/testimonials/edit/<int:testimonial_id>', methods=['GET', 'POST'])
def admin_edit_testimonial(testimonial_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        role = request.form.get('role', '').strip()
        text = request.form.get('text', '').strip()
        stars = int(request.form.get('stars', 5))
        is_active = 1 if request.form.get('is_active') else 0

        if name and role and text:
            cursor.execute(
                'UPDATE testimonials SET name=%s, role=%s, text=%s, stars=%s, is_active=%s WHERE id=%s',
                (name, role, text, stars, is_active, testimonial_id)
            )
            conn.commit()
            conn.close()
            flash('Testimonial updated successfully!', 'success')
            return redirect(url_for('admin_testimonials'))
        else:
            flash('Name, role, and text are required.', 'error')

    cursor.execute('SELECT * FROM testimonials WHERE id = %s', (testimonial_id,))
    testimonial = cursor.fetchone()
    conn.close()

    if testimonial is None:
        flash('Testimonial not found.', 'error')
        return redirect(url_for('admin_testimonials'))

    return render_template('admin_edit_testimonial.html', testimonial=testimonial)


@app.route('/admin/testimonials/delete/<int:testimonial_id>', methods=['POST'])
def admin_delete_testimonial(testimonial_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM testimonials WHERE id = %s', (testimonial_id,))
    conn.commit()
    conn.close()
    flash('Testimonial deleted.', 'success')
    return redirect(url_for('admin_testimonials'))


@app.route('/admin/testimonials/reorder', methods=['POST'])
def admin_reorder_testimonial():
    if not session.get('admin_logged_in'):
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401

    data = request.get_json()
    testimonial_id = data.get('id')
    direction = data.get('direction')  # 'up' or 'down'

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, sort_order FROM testimonials WHERE id = %s', (testimonial_id,))
    current = cursor.fetchone()

    if not current:
        conn.close()
        return jsonify({'success': False, 'error': 'Not found'}), 404

    current_order = current['sort_order']

    if direction == 'up':
        cursor.execute(
            'SELECT id, sort_order FROM testimonials WHERE sort_order < %s ORDER BY sort_order DESC LIMIT 1',
            (current_order,)
        )
    else:
        cursor.execute(
            'SELECT id, sort_order FROM testimonials WHERE sort_order > %s ORDER BY sort_order ASC LIMIT 1',
            (current_order,)
        )
    swap_with = cursor.fetchone()

    if swap_with:
        cursor.execute('UPDATE testimonials SET sort_order = %s WHERE id = %s', (swap_with['sort_order'], current['id']))
        cursor.execute('UPDATE testimonials SET sort_order = %s WHERE id = %s', (current_order, swap_with['id']))
        conn.commit()

    conn.close()
    return jsonify({'success': True})


@app.route('/admin/testimonials/toggle/<int:testimonial_id>', methods=['POST'])
def admin_toggle_testimonial(testimonial_id):
    if not session.get('admin_logged_in'):
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT is_active FROM testimonials WHERE id = %s', (testimonial_id,))
    t = cursor.fetchone()
    if t:
        new_status = 0 if t['is_active'] else 1
        cursor.execute('UPDATE testimonials SET is_active = %s WHERE id = %s', (new_status, testimonial_id))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'is_active': new_status})
    conn.close()
    return jsonify({'success': False}), 404


@app.route('/admin/settings', methods=['GET', 'POST'])
def admin_settings():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        keys = [
            'stat1_value', 'stat1_label',
            'stat2_value', 'stat2_label',
            'stat3_value', 'stat3_label',
            'stat4_value', 'stat4_label',
            'founder_name', 'founder_title',
            'founder_phone', 'founder_email',
            'founder_location',
            'hero_badge', 'hero_title', 'hero_desc',
            'about_subtitle', 'about_desc1', 'about_desc2',
            'about_bullet1', 'about_bullet2', 'about_bullet3',
        ]
        for key in keys:
            value = request.form.get(key, '').strip()
            if value:
                cursor.execute(
                    'INSERT INTO settings (key, value) VALUES (%s, %s) ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value',
                    (key, value)
                )

        # Handle Founder Image Upload
        founder_image_file = request.files.get('founder_image')
        if founder_image_file and founder_image_file.filename:
            processed_path = process_and_crop_image(founder_image_file, app.config['UPLOAD_FOLDER'], aspect_ratio=(4, 5), target_width=800)
            if processed_path:
                cursor.execute(
                    'INSERT INTO settings (key, value) VALUES (%s, %s) ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value',
                    ('founder_image', processed_path)
                )

        conn.commit()
        conn.close()
        flash('Site settings updated successfully!', 'success')
        return redirect(url_for('admin_settings'))

    cursor.execute('SELECT key, value FROM settings')
    all_settings = cursor.fetchall()
    conn.close()
    settings = {row['key']: row['value'] for row in all_settings}
    return render_template('admin_settings.html', settings=settings)


@app.after_request
def add_cache_headers(response):
    # Cache static assets for 1 year (31536000 seconds) to optimize speed
    if request.path.startswith('/static/'):
        response.headers['Cache-Control'] = 'public, max-age=31536000'
    elif request.path.startswith('/admin'):
        # Never cache admin pages so changes always reflect immediately
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate'
    else:
        # Cache public pages for 5 minutes (300 seconds)
        response.headers['Cache-Control'] = 'public, max-age=300'
    return response


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    # Run the Flask development server
    # In production, debug mode will be disabled automatically if FLASK_ENV=production
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    port = int(os.environ.get('PORT', 5001))

    app.run(host='0.0.0.0', debug=debug_mode, port=port)