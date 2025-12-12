
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "change_this_secret_key"  # for flash messages

# Set up Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Hardcoded credentials
VALID_USERNAME = "Fairfield"
VALID_PASSWORD = "ES2025"

@login_manager.user_loader
def load_user(user_id):
    if user_id == VALID_USERNAME:
        return User(user_id)
    return None

DB_PATH = os.path.join(os.path.dirname(__file__), "service.db")


@app.template_filter('aus_date')
def aus_date_filter(date_str):
    """Convert YYYY-MM-DD date string to Australian format DD/MM/YYYY"""
    if not date_str:
        return '—'
    try:
        # Parse the date string (YYYY-MM-DD format)
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        # Return in Australian format DD/MM/YYYY
        return date_obj.strftime("%d/%m/%Y")
    except (ValueError, TypeError):
        # If parsing fails, return original string
        return date_str



def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_number TEXT,
            job_type TEXT,
            customer_name TEXT NOT NULL,
            job_date TEXT,
            location TEXT,
            description TEXT,
            status TEXT,
            notes TEXT,
            labour_hours REAL,
            travel_under_25km INTEGER,
            travel_time_hours REAL,
            travel_cost TEXT
        )
    """)
    
    # Add columns if they don't exist (for existing databases)
    columns_to_add = [
        ("job_number", "TEXT"),
        ("labour_hours", "REAL"),
        ("travel_under_25km", "INTEGER"),
        ("travel_time_hours", "REAL"),
        ("travel_cost", "TEXT")
    ]
    for col_name, col_type in columns_to_add:
        try:
            cur.execute(f"ALTER TABLE jobs ADD COLUMN {col_name} {col_type}")
        except sqlite3.OperationalError:
            pass  # Column already exists
    
    conn.commit()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER,
            name TEXT,
            phone TEXT,
            email TEXT,
            role TEXT,
            FOREIGN KEY(job_id) REFERENCES jobs(id) ON DELETE SET NULL
        )
    """)
    
    # Update existing contacts table to allow NULL job_id if needed
    try:
        cur.execute("ALTER TABLE contacts ALTER COLUMN job_id DROP NOT NULL")
    except sqlite3.OperationalError:
        # SQLite doesn't support ALTER COLUMN, so we'll handle it differently
        # The foreign key constraint will handle SET NULL on delete
        pass

    # Create job_machines table first (needed for migration)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS job_machines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER NOT NULL,
            machine_id INTEGER NOT NULL,
            reported_fault TEXT,
            service_notes TEXT,
            status TEXT,
            FOREIGN KEY(job_id) REFERENCES jobs(id) ON DELETE CASCADE,
            FOREIGN KEY(machine_id) REFERENCES machines(id) ON DELETE CASCADE
        )
    """)
    
    # Check if machines table exists and what columns it has
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='machines'")
    machines_table_exists = cur.fetchone()
    
    if machines_table_exists:
        cur.execute("PRAGMA table_info(machines)")
        machine_columns_info = cur.fetchall()
        machine_columns = [col[1] for col in machine_columns_info]
        
        # Check if job_id is NOT NULL
        job_id_not_null = any(col[1] == "job_id" and col[3] == 1 for col in machine_columns_info)
        
        # If job_id is NOT NULL, we need to recreate the table to make it nullable
        if job_id_not_null:
            # Create temporary table with correct schema
            cur.execute("""
                CREATE TABLE machines_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_name TEXT,
                    model TEXT,
                    serial_number TEXT,
                    reported_fault TEXT,
                    service_notes TEXT,
                    status TEXT,
                    job_id INTEGER,
                    UNIQUE(customer_name, serial_number)
                )
            """)
            
            # Copy data from old table
            cur.execute("""
                INSERT INTO machines_new (id, customer_name, model, serial_number, reported_fault, service_notes, status, job_id)
                SELECT id, customer_name, model, serial_number, reported_fault, service_notes, status, job_id
                FROM machines
            """)
            
            # Drop old table
            cur.execute("DROP TABLE machines")
            
            # Rename new table
            cur.execute("ALTER TABLE machines_new RENAME TO machines")
            conn.commit()
        
        # Ensure customer_name column exists
        if "customer_name" not in machine_columns:
            try:
                cur.execute("ALTER TABLE machines ADD COLUMN customer_name TEXT")
                conn.commit()
            except sqlite3.OperationalError:
                pass
        
        # Populate customer_name from jobs if missing
        cur.execute("""
            UPDATE machines 
            SET customer_name = (SELECT customer_name FROM jobs WHERE jobs.id = machines.job_id)
            WHERE customer_name IS NULL AND job_id IS NOT NULL
        """)
        conn.commit()
        
        # Migrate to job_machines if not already done
        cur.execute("SELECT COUNT(*) FROM job_machines")
        job_machines_count = cur.fetchone()[0]
        if job_machines_count == 0:
            cur.execute("""
                INSERT INTO job_machines (job_id, machine_id, reported_fault, service_notes, status)
                SELECT job_id, id, reported_fault, service_notes, status
                FROM machines
                WHERE job_id IS NOT NULL
            """)
            conn.commit()
    else:
        # Create new machines table with customer_name
        cur.execute("""
            CREATE TABLE machines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT,
                model TEXT,
                serial_number TEXT,
                reported_fault TEXT,
                service_notes TEXT,
                status TEXT,
                job_id INTEGER,
                UNIQUE(customer_name, serial_number)
            )
        """)
        conn.commit()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS parts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER NOT NULL,
            machine_id INTEGER,
            machine_serial TEXT,
            part_number TEXT,
            description TEXT,
            quantity REAL,
            unit_price REAL,
            FOREIGN KEY(job_id) REFERENCES jobs(id) ON DELETE CASCADE,
            FOREIGN KEY(machine_id) REFERENCES machines(id) ON DELETE SET NULL
        )
    """)
    
    # Add machine_id column if it doesn't exist (for existing databases)
    try:
        cur.execute("ALTER TABLE parts ADD COLUMN machine_id INTEGER")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    # Add machine_serial column if it doesn't exist
    try:
        cur.execute("ALTER TABLE parts ADD COLUMN machine_serial TEXT")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    # Add unit_price column if it doesn't exist (kept for compatibility)
    try:
        cur.execute("ALTER TABLE parts ADD COLUMN unit_price REAL")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    # Add head column if it doesn't exist
    try:
        cur.execute("ALTER TABLE parts ADD COLUMN head TEXT")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    # Create parts_catalog table for the parts catalog
    cur.execute("""
        CREATE TABLE IF NOT EXISTS parts_catalog (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            part_number TEXT NOT NULL UNIQUE,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()


# Initialize database on startup
init_db()


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            user = User(username)
            login_user(user)
            flash("Login successful!", "success")
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for("list_jobs"))
        else:
            flash("Invalid username or password.", "danger")
    
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

@app.route("/")
def index():
    return redirect(url_for("list_jobs"))


@app.route("/jobs")
@login_required
def list_jobs():
    search_query = request.args.get("search", "").strip()
    conn = get_db()
    cur = conn.cursor()
    
    if search_query:
        cur.execute("""
            SELECT * FROM jobs 
            WHERE customer_name LIKE ? 
            ORDER BY CASE WHEN job_date IS NULL THEN 1 ELSE 0 END, job_date DESC, id DESC
        """, (f"%{search_query}%",))
    else:
        cur.execute("SELECT * FROM jobs ORDER BY CASE WHEN job_date IS NULL THEN 1 ELSE 0 END, job_date DESC, id DESC")
    
    jobs = cur.fetchall()
    conn.close()
    return render_template("jobs_list.html", jobs=jobs, search_query=search_query)


@app.route("/jobs/<int:job_id>/delete", methods=["POST"])
@login_required
def delete_job(job_id):
    conn = get_db()
    cur = conn.cursor()
    
    # Verify job exists
    cur.execute("SELECT id FROM jobs WHERE id = ?", (job_id,))
    if not cur.fetchone():
        conn.close()
        flash("Job not found.", "danger")
        return redirect(url_for("list_jobs"))
    
    # Delete parts and job_machines for this job (contacts will be kept with job_id set to NULL)
    # Note: We don't delete machines themselves as they belong to customers, not jobs
    cur.execute("DELETE FROM parts WHERE job_id = ?", (job_id,))
    cur.execute("DELETE FROM job_machines WHERE job_id = ?", (job_id,))
    
    # Set contacts job_id to NULL instead of deleting them
    cur.execute("UPDATE contacts SET job_id = NULL WHERE job_id = ?", (job_id,))
    
    # Delete the job
    cur.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
    conn.commit()
    conn.close()
    
    flash("Job deleted (parts and job machines removed, contacts preserved).", "success")
    return redirect(url_for("list_jobs"))


@app.route("/jobs/new", methods=["GET", "POST"])
@login_required
def new_job():
    if request.method == "POST":
        job_number = request.form.get("job_number")
        job_type = request.form.get("job_type")
        customer_name = request.form.get("customer_name")
        job_date = request.form.get("job_date")
        location = request.form.get("location")
        description = request.form.get("description")
        status = request.form.get("status")
        notes = request.form.get("notes")
        labour_hours = request.form.get("labour_hours")
        travel_under_25km = request.form.get("travel_under_25km")
        travel_time_hours = request.form.get("travel_time_hours")
        travel_cost = request.form.get("travel_cost")

        if not customer_name or not customer_name.strip():
            flash("Customer name is required.", "danger")
            return redirect(url_for("new_job"))
        
        if not job_number or not job_number.strip():
            flash("Job number is required.", "danger")
            return redirect(url_for("new_job"))
        
        # Check for duplicate job number
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id FROM jobs WHERE job_number = ?", (job_number.strip(),))
        if cur.fetchone():
            conn.close()
            flash(f"Job number '{job_number.strip()}' already exists. Please use a different job number.", "danger")
            return redirect(url_for("new_job"))
        conn.close()

        try:
            labour_val = float(labour_hours) if labour_hours else None
        except ValueError:
            labour_val = None
        
        travel_under_25_val = 1 if travel_under_25km == "yes" else 0
        
        try:
            travel_time_val = float(travel_time_hours) if travel_time_hours else None
        except ValueError:
            travel_time_val = None
        
        # Travel cost can be text (for "calculated later") or number
        travel_cost_val = travel_cost.strip() if travel_cost and travel_cost.strip() else None

        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO jobs (job_number, job_type, customer_name, job_date, location, description, status, notes, labour_hours, travel_under_25km, travel_time_hours, travel_cost)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (job_number, job_type, customer_name, job_date, location, description, status, notes, labour_val, travel_under_25_val, travel_time_val, travel_cost_val),
        )
        conn.commit()
        job_id = cur.lastrowid
        conn.close()

        flash("Job created.", "success")
        return redirect(url_for("job_detail", job_id=job_id))

    # GET
    today_str = datetime.today().strftime("%Y-%m-%d")
    return render_template("job_form.html", today=today_str)


@app.route("/jobs/<int:job_id>")
@login_required
def job_detail(job_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
    job = cur.fetchone()
    if not job:
        conn.close()
        flash("Job not found.", "danger")
        return redirect(url_for("list_jobs"))

    cur.execute("SELECT * FROM contacts WHERE job_id = ? ORDER BY id", (job_id,))
    contacts = cur.fetchall()

    # Get machines for this job (through job_machines)
    # Order by job_machine.id so each entry appears in the order it was added
    # Explicitly select columns to avoid conflicts with job_machines columns
    cur.execute("""
        SELECT m.id as machine_id, m.customer_name, m.model, m.serial_number,
               jm.reported_fault, jm.service_notes, jm.status, jm.id as job_machine_id
        FROM machines m
        JOIN job_machines jm ON m.id = jm.machine_id
        WHERE jm.job_id = ?
        ORDER BY jm.id
    """, (job_id,))
    machines = cur.fetchall()
    
    # Also get all machines for this customer for dropdowns
    customer_machines = []
    if job:
        cur.execute("""
            SELECT * FROM machines 
            WHERE customer_name = ? 
            ORDER BY serial_number, model
        """, (job["customer_name"],))
        customer_machines = cur.fetchall()

    cur.execute("SELECT * FROM parts WHERE job_id = ? ORDER BY id", (job_id,))
    parts = cur.fetchall()

    # Calculate travel info
    try:
        travel_under_25 = bool(job["travel_under_25km"] or 0)
    except (KeyError, IndexError):
        travel_under_25 = False
    
    try:
        travel_time_hours = job["travel_time_hours"] or 0
    except (KeyError, IndexError):
        travel_time_hours = 0
    
    conn.close()
    return render_template(
        "job_detail.html",
        job=job,
        contacts=contacts,
        machines=machines,
        customer_machines=customer_machines,
        parts=parts,
        travel_under_25=travel_under_25,
        travel_time_hours=travel_time_hours,
    )


@app.route("/jobs/<int:job_id>/update_field", methods=["POST"])
@login_required
def update_job_field(job_id):
    field = request.form.get("field")
    value = request.form.get("value")
    
    # Map field names to database columns
    field_map = {
        "type": "job_type",
        "date": "job_date",
        "status": "status",
        "location": "location",
        "description": "description",
        "job_number": "job_number",
        "travel_cost": "travel_cost"
    }
    
    if field not in field_map:
        flash("Invalid field.", "danger")
        return redirect(url_for("job_detail", job_id=job_id))
    
    db_field = field_map[field]
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id FROM jobs WHERE id = ?", (job_id,))
    if not cur.fetchone():
        conn.close()
        flash("Job not found.", "danger")
        return redirect(url_for("list_jobs"))
    
    # Use parameterized query with column name validation
    if db_field == "job_type":
        cur.execute("UPDATE jobs SET job_type = ? WHERE id = ?", (value if value else None, job_id))
    elif db_field == "job_date":
        cur.execute("UPDATE jobs SET job_date = ? WHERE id = ?", (value if value else None, job_id))
    elif db_field == "status":
        cur.execute("UPDATE jobs SET status = ? WHERE id = ?", (value if value else None, job_id))
    elif db_field == "location":
        cur.execute("UPDATE jobs SET location = ? WHERE id = ?", (value if value else None, job_id))
    elif db_field == "description":
        cur.execute("UPDATE jobs SET description = ? WHERE id = ?", (value if value else None, job_id))
    elif db_field == "job_number":
        # Job number should not be empty
        if not value or not value.strip():
            flash("Job number cannot be empty.", "danger")
            conn.close()
            referer = request.headers.get("Referer")
            if referer and "list_jobs" in referer:
                return redirect(url_for("list_jobs"))
            return redirect(url_for("job_detail", job_id=job_id))
        cur.execute("UPDATE jobs SET job_number = ? WHERE id = ?", (value.strip(), job_id))
    elif db_field == "travel_cost":
        # Travel cost can be text (for "calculated later") or number
        travel_cost_val = value.strip() if value and value.strip() else None
        cur.execute("UPDATE jobs SET travel_cost = ? WHERE id = ?", (travel_cost_val, job_id))
    
    conn.commit()
    conn.close()
    
    flash("Job updated.", "success")
    # Check if request came from jobs list page
    from_page = request.form.get("from_page") or request.args.get("from")
    if from_page == "list_jobs":
        return redirect(url_for("list_jobs"))
    # Also check referer header as fallback
    referer = request.headers.get("Referer")
    if referer and ("/jobs" in referer and "/jobs/" not in referer.split("?")[0]):
        return redirect(url_for("list_jobs"))
    return redirect(url_for("job_detail", job_id=job_id))


@app.route("/jobs/<int:job_id>/update_travel", methods=["POST"])
@login_required
def update_travel(job_id):
    """Update travel information for a job"""
    travel_type = request.form.get("travel_type")
    travel_time_hours = request.form.get("travel_time_hours")
    travel_cost = request.form.get("travel_cost")
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id FROM jobs WHERE id = ?", (job_id,))
    if not cur.fetchone():
        conn.close()
        flash("Job not found.", "danger")
        return redirect(url_for("list_jobs"))
    
    if travel_type == "under_25km":
        cur.execute("UPDATE jobs SET travel_under_25km = ?, travel_time_hours = ?, travel_cost = ? WHERE id = ?", 
                   (1, None, None, job_id))
    elif travel_type == "hours":
        try:
            travel_time_val = float(travel_time_hours) if travel_time_hours else None
        except ValueError:
            travel_time_val = None
        cur.execute("UPDATE jobs SET travel_under_25km = ?, travel_time_hours = ?, travel_cost = ? WHERE id = ?", 
                   (0, travel_time_val, None, job_id))
    elif travel_type == "calculated_later":
        travel_cost_val = travel_cost.strip() if travel_cost and travel_cost.strip() else None
        cur.execute("UPDATE jobs SET travel_under_25km = ?, travel_time_hours = ?, travel_cost = ? WHERE id = ?", 
                   (0, None, travel_cost_val, job_id))
    else:
        # Invalid travel_type
        conn.close()
        flash("Invalid travel type.", "danger")
        return redirect(url_for("job_detail", job_id=job_id))
    
    conn.commit()
    conn.close()
    
    flash("Travel information updated.", "success")
    return redirect(url_for("job_detail", job_id=job_id))


@app.route("/jobs/<int:job_id>/add_contact", methods=["POST"])
@login_required
def add_contact(job_id):
    name = request.form.get("name")
    phone = request.form.get("phone")
    email = request.form.get("email")
    role = request.form.get("role")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id FROM jobs WHERE id = ?", (job_id,))
    if not cur.fetchone():
        conn.close()
        flash("Job not found.", "danger")
        return redirect(url_for("list_jobs"))

    cur.execute(
        """
        INSERT INTO contacts (job_id, name, phone, email, role)
        VALUES (?, ?, ?, ?, ?)
        """,
        (job_id, name, phone, email, role),
    )
    conn.commit()
    conn.close()

    flash("Contact added.", "success")
    return redirect(url_for("job_detail", job_id=job_id))


@app.route("/jobs/<int:job_id>/add_machine", methods=["POST"])
@login_required
def add_machine(job_id):
    # Get form values directly from request - no caching, no defaults
    # Use .get() which returns None if key doesn't exist, then handle empty strings
    machine_id_raw = request.form.get("machine_id")
    machine_id = machine_id_raw.strip() if machine_id_raw else ""
    
    model_raw = request.form.get("model")
    model = model_raw.strip() if model_raw else ""
    
    serial_number_raw = request.form.get("serial_number")
    serial_number = serial_number_raw.strip() if serial_number_raw else ""
    
    # Get textarea/select values - empty string becomes None for database
    reported_fault_raw = request.form.get("reported_fault")
    reported_fault = reported_fault_raw.strip() if reported_fault_raw and reported_fault_raw.strip() else None
    
    service_notes_raw = request.form.get("service_notes")
    service_notes = service_notes_raw.strip() if service_notes_raw and service_notes_raw.strip() else None
    
    status_raw = request.form.get("status")
    status = status_raw.strip() if status_raw and status_raw.strip() else None
    

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, customer_name FROM jobs WHERE id = ?", (job_id,))
    job = cur.fetchone()
    if not job:
        conn.close()
        flash("Job not found.", "danger")
        return redirect(url_for("list_jobs"))

    customer_name = job["customer_name"]
    
    # If machine_id provided, use existing machine, otherwise create/find machine
    if machine_id:
        try:
            machine_id_val = int(machine_id.strip())
        except ValueError:
            conn.close()
            flash("Invalid machine ID.", "danger")
            return redirect(url_for("job_detail", job_id=job_id))
        # Verify machine exists
        cur.execute("SELECT id, customer_name FROM machines WHERE id = ?", (machine_id_val,))
        machine = cur.fetchone()
        if not machine:
            conn.close()
            flash("Machine not found.", "danger")
            return redirect(url_for("job_detail", job_id=job_id))
        # Update customer_name if it doesn't match (for migration compatibility)
        if machine["customer_name"] != customer_name:
            cur.execute("UPDATE machines SET customer_name = ? WHERE id = ?", (customer_name, machine_id_val))
            conn.commit()
        # Ignore model/serial_number fields when machine_id is provided - use the existing machine as-is
    else:
        # Create new machine or find existing one by serial number
        if not serial_number or not serial_number.strip():
            conn.close()
            flash("Serial number is required when adding a new machine.", "danger")
            return redirect(url_for("job_detail", job_id=job_id))
        
        # Check if machine already exists for this customer by serial number
        cur.execute("SELECT id FROM machines WHERE customer_name = ? AND serial_number = ?", (customer_name, serial_number.strip()))
        existing = cur.fetchone()
        if existing:
            machine_id_val = existing["id"]
            # Update model if provided and different
            if model and model.strip():
                cur.execute("UPDATE machines SET model = ? WHERE id = ? AND (model IS NULL OR model != ?)", (model.strip(), machine_id_val, model.strip()))
                conn.commit()
        else:
            # Create new machine - customer_name is required
            if not customer_name or not customer_name.strip():
                conn.close()
                flash("Customer name is required.", "danger")
                return redirect(url_for("job_detail", job_id=job_id))
            
            cur.execute(
                """
                INSERT INTO machines (customer_name, model, serial_number)
                VALUES (?, ?, ?)
                """,
                (customer_name.strip(), model.strip() if model else None, serial_number.strip()),
            )
            machine_id_val = cur.lastrowid
            conn.commit()
    
    # Create job_machine entry with job-specific work
    # Note: Same machine can be added multiple times to a job (e.g., for different issues/work)
    # Use the exact form values - ensure empty strings become None
    reported_fault_val = reported_fault if reported_fault else None
    service_notes_val = service_notes if service_notes else None
    status_val = status if status else None
    
    cur.execute(
        """
        INSERT INTO job_machines (job_id, machine_id, reported_fault, service_notes, status)
        VALUES (?, ?, ?, ?, ?)
        """,
        (job_id, machine_id_val, reported_fault_val, service_notes_val, status_val),
    )
    conn.commit()
    
    conn.close()

    flash("Machine added to job.", "success")
    return redirect(url_for("job_detail", job_id=job_id))


@app.route("/jobs/<int:job_id>/add_part", methods=["POST"])
@login_required
def add_part(job_id):
    machine_id = request.form.get("machine_id")
    part_number = request.form.get("part_number")
    description = request.form.get("description")
    head = request.form.get("head")
    quantity = request.form.get("quantity")
    
    # Validate that part_number exists in the parts catalog
    if part_number:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT part_number FROM parts_catalog WHERE part_number = ?", (part_number,))
        if not cur.fetchone():
            conn.close()
            flash("Part number must be selected from the catalog. Random part numbers are not allowed.", "danger")
            return redirect(url_for("job_detail", job_id=job_id))
        conn.close()

    try:
        quantity_val = int(quantity) if quantity else 1
    except ValueError:
        quantity_val = 1

    # Get machine serial from selected machine
    machine_id_val = None
    machine_serial = None
    if machine_id and machine_id != "":
        try:
            machine_id_val = int(machine_id)
            conn = get_db()
            cur = conn.cursor()
            cur.execute("SELECT serial_number FROM machines WHERE id = ?", (machine_id_val,))
            machine = cur.fetchone()
            if machine:
                machine_serial = machine[0] if machine[0] else None
            conn.close()
        except ValueError:
            machine_id_val = None

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id FROM jobs WHERE id = ?", (job_id,))
    if not cur.fetchone():
        conn.close()
        flash("Job not found.", "danger")
        return redirect(url_for("list_jobs"))

    cur.execute(
        """
        INSERT INTO parts (job_id, machine_id, machine_serial, part_number, description, head, quantity, unit_price)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (job_id, machine_id_val, machine_serial, part_number, description, head.strip() if head else None, quantity_val, None),
    )
    conn.commit()
    conn.close()

    flash("Part added.", "success")
    return redirect(url_for("job_detail", job_id=job_id))


@app.route("/contacts/<int:contact_id>/edit", methods=["GET", "POST"])
@login_required
def edit_contact(contact_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,))
    contact = cur.fetchone()
    if not contact:
        conn.close()
        flash("Contact not found.", "danger")
        return redirect(url_for("list_jobs"))
    
    job_id = contact["job_id"]
    
    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        email = request.form.get("email")
        role = request.form.get("role")
        
        cur.execute(
            """
            UPDATE contacts
            SET name = ?, phone = ?, email = ?, role = ?
            WHERE id = ?
            """,
            (name, phone, email, role, contact_id),
        )
        conn.commit()
        conn.close()
        flash("Contact updated.", "success")
        return redirect(url_for("job_detail", job_id=job_id))
    
    conn.close()
    return render_template("contact_edit_form.html", contact=contact)


@app.route("/contacts/<int:contact_id>/delete", methods=["POST"])
@login_required
def delete_contact(contact_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT job_id FROM contacts WHERE id = ?", (contact_id,))
    contact = cur.fetchone()
    if not contact:
        conn.close()
        flash("Contact not found.", "danger")
        return redirect(url_for("list_jobs"))
    
    job_id = contact["job_id"]
    cur.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    conn.commit()
    conn.close()
    flash("Contact deleted.", "success")
    return redirect(url_for("job_detail", job_id=job_id))


@app.route("/job_machines/<int:job_machine_id>/edit", methods=["GET", "POST"])
@login_required
def edit_machine(job_machine_id):
    conn = get_db()
    cur = conn.cursor()
    # Get job_machine with machine details
    cur.execute("""
        SELECT jm.*, m.model, m.serial_number, m.customer_name
        FROM job_machines jm
        JOIN machines m ON jm.machine_id = m.id
        WHERE jm.id = ?
    """, (job_machine_id,))
    job_machine = cur.fetchone()
    if not job_machine:
        conn.close()
        flash("Machine entry not found.", "danger")
        return redirect(url_for("list_jobs"))
    
    job_id = job_machine["job_id"]
    
    if request.method == "POST":
        reported_fault = request.form.get("reported_fault")
        service_notes = request.form.get("service_notes")
        status = request.form.get("status")
        
        # Update job_machines (job-specific work)
        cur.execute(
            """
            UPDATE job_machines
            SET reported_fault = ?, service_notes = ?, status = ?
            WHERE id = ?
            """,
            (reported_fault, service_notes, status, job_machine_id),
        )
        
        # Also update machine model if changed (customer-level info)
        model = request.form.get("model")
        if model:
            cur.execute("UPDATE machines SET model = ? WHERE id = ?", (model, job_machine["machine_id"]))
        
        conn.commit()
        conn.close()
        flash("Machine updated.", "success")
        return redirect(url_for("job_detail", job_id=job_id))
    
    conn.close()
    # Create a combined object for the template
    machine = {
        "id": job_machine["machine_id"],
        "job_machine_id": job_machine_id,
        "job_id": job_id,
        "model": job_machine["model"],
        "serial_number": job_machine["serial_number"],
        "reported_fault": job_machine["reported_fault"],
        "service_notes": job_machine["service_notes"],
        "status": job_machine["status"]
    }
    return render_template("machine_edit_form.html", machine=machine)


@app.route("/job_machines/<int:job_machine_id>/delete", methods=["POST"])
@login_required
def delete_machine(job_machine_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT job_id FROM job_machines WHERE id = ?", (job_machine_id,))
    job_machine = cur.fetchone()
    if not job_machine:
        conn.close()
        flash("Machine entry not found.", "danger")
        return redirect(url_for("list_jobs"))
    
    job_id = job_machine["job_id"]
    # Delete only the job_machine entry, not the machine itself (machine belongs to customer)
    cur.execute("DELETE FROM job_machines WHERE id = ?", (job_machine_id,))
    conn.commit()
    conn.close()
    flash("Machine removed from job.", "success")
    return redirect(url_for("job_detail", job_id=job_id))


@app.route("/parts/<int:part_id>/edit", methods=["GET", "POST"])
@login_required
def edit_part(part_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM parts WHERE id = ?", (part_id,))
    part = cur.fetchone()
    if not part:
        conn.close()
        flash("Part not found.", "danger")
        return redirect(url_for("list_jobs"))
    
    job_id = part["job_id"]
    cur.execute("SELECT id, customer_name FROM jobs WHERE id = ?", (job_id,))
    job = cur.fetchone()
    
    # Get all machines for this customer (not just job machines)
    cur.execute("""
        SELECT *
        FROM machines
        WHERE customer_name = ?
        ORDER BY serial_number, model
    """, (job["customer_name"],))
    machines = cur.fetchall()
    
    if request.method == "POST":
        machine_id = request.form.get("machine_id")
        part_number = request.form.get("part_number")
        description = request.form.get("description")
        head = request.form.get("head")
        quantity = request.form.get("quantity")
        
        # Validate that part_number exists in the parts catalog
        if part_number:
            cur.execute("SELECT part_number FROM parts_catalog WHERE part_number = ?", (part_number,))
            if not cur.fetchone():
                conn.close()
                flash("Part number must be selected from the catalog. Random part numbers are not allowed.", "danger")
                return redirect(url_for("edit_part", part_id=part_id))
        
        try:
            quantity_val = int(quantity) if quantity else 1
        except ValueError:
            quantity_val = 1
        
        machine_id_val = None
        machine_serial = None
        if machine_id and machine_id != "":
            try:
                machine_id_val = int(machine_id)
                cur.execute("SELECT serial_number FROM machines WHERE id = ?", (machine_id_val,))
                machine = cur.fetchone()
                if machine:
                    machine_serial = machine[0] if machine[0] else None
            except ValueError:
                machine_id_val = None
        
        cur.execute(
            """
            UPDATE parts
            SET machine_id = ?, machine_serial = ?, part_number = ?, description = ?, head = ?, quantity = ?, unit_price = ?
            WHERE id = ?
            """,
            (machine_id_val, machine_serial, part_number, description, head.strip() if head else None, quantity_val, None, part_id),
        )
        conn.commit()
        conn.close()
        flash("Part updated.", "success")
        return redirect(url_for("job_detail", job_id=job_id))
    
    conn.close()
    return render_template("part_edit_form.html", part=part, machines=machines)


@app.route("/parts/<int:part_id>/delete", methods=["POST"])
@login_required
def delete_part(part_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT job_id FROM parts WHERE id = ?", (part_id,))
    part = cur.fetchone()
    if not part:
        conn.close()
        flash("Part not found.", "danger")
        return redirect(url_for("list_jobs"))
    
    job_id = part["job_id"]
    cur.execute("DELETE FROM parts WHERE id = ?", (part_id,))
    conn.commit()
    conn.close()
    flash("Part deleted.", "success")
    return redirect(url_for("job_detail", job_id=job_id))


@app.route("/machines/search")
@login_required
def search_machines():
    query = request.args.get("q", "").strip()
    
    if not query:
        return render_template("machine_search.html", machines=[], query="")
    
    conn = get_db()
    cur = conn.cursor()
    
    # Search by both model and serial number
    # Updated to use the new schema where machines are customer-centric
    cur.execute(
        """
        SELECT DISTINCT 
            m.id,
            m.serial_number, 
            m.model,
            m.customer_name,
            (SELECT j.job_date 
             FROM job_machines jm
             JOIN jobs j ON jm.job_id = j.id
             WHERE jm.machine_id = m.id
             ORDER BY j.job_date DESC, j.id DESC 
             LIMIT 1) as last_job_date
        FROM machines m
        WHERE (m.model LIKE ? OR m.serial_number LIKE ?)
        ORDER BY last_job_date DESC, m.serial_number
        """,
        (f"%{query}%", f"%{query}%")
    )
    machines = cur.fetchall()
    conn.close()
    
    return render_template("machine_search.html", machines=machines, query=query)


@app.route("/machines/<int:machine_id>/edit", methods=["GET", "POST"])
@login_required
def edit_machine_base(machine_id):
    """Edit a machine's base information (model, serial number, customer)"""
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM machines WHERE id = ?", (machine_id,))
    machine = cur.fetchone()
    if not machine:
        conn.close()
        flash("Machine not found.", "danger")
        return redirect(url_for("search_machines"))
    
    if request.method == "POST":
        model = request.form.get("model", "").strip() or None
        serial_number = request.form.get("serial_number", "").strip() or None
        customer_name = request.form.get("customer_name", "").strip()
        
        if not customer_name:
            conn.close()
            flash("Customer name is required.", "danger")
            return redirect(url_for("edit_machine_base", machine_id=machine_id))
        
        # Check if serial number already exists for this customer (excluding current machine)
        if serial_number:
            cur.execute("""
                SELECT id FROM machines 
                WHERE customer_name = ? AND serial_number = ? AND id != ?
            """, (customer_name, serial_number, machine_id))
            existing = cur.fetchone()
            if existing:
                conn.close()
                flash("A machine with this serial number already exists for this customer.", "danger")
                return redirect(url_for("edit_machine_base", machine_id=machine_id))
        
        cur.execute("""
            UPDATE machines 
            SET model = ?, serial_number = ?, customer_name = ?
            WHERE id = ?
        """, (model, serial_number, customer_name, machine_id))
        
        conn.commit()
        conn.close()
        flash("Machine updated.", "success")
        return redirect(url_for("search_machines", q=serial_number or model or ""))
    
    conn.close()
    return render_template("machine_base_edit_form.html", machine=machine)


@app.route("/machines/<int:machine_id>/delete", methods=["POST"])
@login_required
def delete_machine_base(machine_id):
    """Delete a machine (only if it has no job associations)"""
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM machines WHERE id = ?", (machine_id,))
    machine = cur.fetchone()
    if not machine:
        conn.close()
        flash("Machine not found.", "danger")
        return redirect(url_for("search_machines"))
    
    # Check if machine is used in any jobs
    cur.execute("SELECT COUNT(*) as count FROM job_machines WHERE machine_id = ?", (machine_id,))
    job_count = cur.fetchone()["count"]
    
    if job_count > 0:
        conn.close()
        flash(f"Cannot delete machine: it is associated with {job_count} job(s). Remove it from jobs first.", "danger")
        return redirect(url_for("search_machines"))
    
    serial_number = machine["serial_number"] or ""
    cur.execute("DELETE FROM machines WHERE id = ?", (machine_id,))
    conn.commit()
    conn.close()
    
    flash("Machine deleted.", "success")
    return redirect(url_for("search_machines"))


@app.route("/machines/<serial_number>/jobs")
@login_required
def machine_jobs(serial_number):
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute(
        """
        SELECT DISTINCT m.model, m.serial_number
        FROM machines m
        WHERE m.serial_number = ?
        LIMIT 1
        """,
        (serial_number,)
    )
    machine_info = cur.fetchone()
    
    if not machine_info:
        conn.close()
        flash("Machine not found.", "danger")
        return redirect(url_for("search_machines"))
    
    cur.execute(
        """
        SELECT DISTINCT j.*, jm.reported_fault
        FROM jobs j
        JOIN job_machines jm ON j.id = jm.job_id
        JOIN machines m ON jm.machine_id = m.id
        WHERE m.serial_number = ?
        ORDER BY j.job_date DESC, j.id DESC
        """,
        (serial_number,)
    )
    jobs = cur.fetchall()
    conn.close()
    
    return render_template("machine_jobs_list.html", 
                         machine_info=machine_info, 
                         jobs=jobs, 
                         serial_number=serial_number)


@app.route("/customers")
@login_required
def list_customers():
    search_query = request.args.get("search", "").strip()
    conn = get_db()
    cur = conn.cursor()
    
    # Base query for customer info with most recent location and contact details
    base_query = """
        SELECT DISTINCT 
            j1.customer_name,
            (SELECT location FROM jobs j2 
             WHERE j2.customer_name = j1.customer_name 
             AND j2.location IS NOT NULL 
             AND j2.location != ''
             ORDER BY j2.job_date DESC, j2.id DESC 
             LIMIT 1) as location,
            (SELECT name FROM contacts c
             WHERE c.job_id IN (SELECT id FROM jobs WHERE customer_name = j1.customer_name)
             AND c.name IS NOT NULL
             AND c.name != ''
             ORDER BY c.id DESC
             LIMIT 1) as contact_name,
            (SELECT phone FROM contacts c
             WHERE c.job_id IN (SELECT id FROM jobs WHERE customer_name = j1.customer_name)
             AND c.phone IS NOT NULL
             AND c.phone != ''
             ORDER BY c.id DESC
             LIMIT 1) as contact_phone
        FROM jobs j1
    """
    
    if search_query:
        # Search in customer_name, location, contact_name, or contact_phone
        # We'll filter after fetching since we need subqueries for location/contacts
        cur.execute(base_query + "ORDER BY customer_name")
        all_customers = cur.fetchall()
        
        # Filter customers based on search query
        search_lower = search_query.lower()
        customers = []
        for customer in all_customers:
            # Safely access dictionary keys with None checks
            customer_name = customer.get("customer_name", "") or ""
            location = customer.get("location") or ""
            contact_name = customer.get("contact_name") or ""
            contact_phone = customer.get("contact_phone") or ""
            
            if (search_lower in customer_name.lower() or
                (location and search_lower in location.lower()) or
                (contact_name and search_lower in contact_name.lower()) or
                (contact_phone and search_lower in contact_phone.lower())):
                customers.append(customer)
    else:
        cur.execute(base_query + "ORDER BY customer_name")
        customers = cur.fetchall()
    
    conn.close()
    return render_template("customers_list.html", customers=customers, search_query=search_query)


@app.route("/customers/<customer_name>/jobs")
@login_required
def customer_jobs(customer_name):
    conn = get_db()
    cur = conn.cursor()
    
    # Get all jobs for this customer
    cur.execute("SELECT * FROM jobs WHERE customer_name = ? ORDER BY job_date DESC, id DESC", (customer_name,))
    jobs = cur.fetchall()
    
    # Get customer info
    cur.execute("""
        SELECT 
            customer_name,
            (SELECT location FROM jobs j2 
             WHERE j2.customer_name = ? 
             AND j2.location IS NOT NULL 
             AND j2.location != ''
             ORDER BY j2.job_date DESC, j2.id DESC 
             LIMIT 1) as location
        FROM jobs
        WHERE customer_name = ?
        LIMIT 1
    """, (customer_name, customer_name))
    customer_info = cur.fetchone()
    
    conn.close()
    
    if not customer_info:
        flash("Customer not found.", "danger")
        return redirect(url_for("list_customers"))
    
    return render_template("customer_jobs_list.html", jobs=jobs, customer_name=customer_name, customer_info=customer_info)


@app.route("/api/customers/search")
@login_required
def search_customers():
    """API endpoint for customer autocomplete"""
    query = request.args.get("q", "").strip().lower()
    if not query:
        return jsonify([])
    
    conn = get_db()
    cur = conn.cursor()
    # Get distinct customer names and their most recent location
    cur.execute("""
        SELECT DISTINCT 
            customer_name,
            (SELECT location FROM jobs j2 
             WHERE j2.customer_name = j1.customer_name 
             AND j2.location IS NOT NULL 
             AND j2.location != ''
             ORDER BY j2.job_date DESC, j2.id DESC 
             LIMIT 1) as location
        FROM jobs j1
        WHERE LOWER(customer_name) LIKE ?
        ORDER BY customer_name
        LIMIT 10
    """, (f"%{query}%",))
    
    results = []
    for row in cur.fetchall():
        results.append({
            "name": row["customer_name"],
            "location": row["location"] or ""
        })
    
    conn.close()
    return jsonify(results)


@app.route("/api/parts/search")
@login_required
def search_parts():
    """API endpoint to search for parts by part number from the parts catalog"""
    query = request.args.get("q", "").strip()
    
    if not query or len(query) < 2:
        return jsonify([])
    
    conn = get_db()
    cur = conn.cursor()
    
    # Search in the parts_catalog table
    cur.execute("""
        SELECT part_number, description
        FROM parts_catalog
        WHERE part_number LIKE ? AND part_number IS NOT NULL AND part_number != ''
        ORDER BY part_number
        LIMIT 20
    """, (f"%{query}%",))
    
    parts = cur.fetchall()
    conn.close()
    
    # Convert to list of dictionaries
    results = []
    for part in parts:
        results.append({
            "part_number": part["part_number"],
            "description": part["description"] or ""
        })
    
    return jsonify(results)


@app.route("/api/machines/list")
@login_required
def list_machines_api():
    """API endpoint to get all existing machines"""
    conn = get_db()
    cur = conn.cursor()
    # Get distinct machines by serial number with their most recent model
    cur.execute("""
        SELECT DISTINCT 
            serial_number,
            (SELECT model FROM machines m2 
             WHERE m2.serial_number = m1.serial_number 
             AND m2.model IS NOT NULL 
             AND m2.model != ''
             ORDER BY m2.id DESC 
             LIMIT 1) as model
        FROM machines m1
        WHERE serial_number IS NOT NULL 
        AND serial_number != ''
        ORDER BY serial_number
    """)
    
    results = []
    for row in cur.fetchall():
        results.append({
            "serial_number": row["serial_number"],
            "model": row["model"] or ""
        })
    
    conn.close()
    return jsonify(results)


@app.route("/jobs/<int:job_id>/export")
@login_required
def export_job(job_id):
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
    job = cur.fetchone()
    if not job:
        conn.close()
        flash("Job not found.", "danger")
        return redirect(url_for("list_jobs"))
    
    cur.execute("SELECT * FROM contacts WHERE job_id = ? ORDER BY id", (job_id,))
    contacts = cur.fetchall()
    
    # Get machines for this job (through job_machines)
    # Order by job_machine.id so each entry appears in the order it was added
    # Explicitly select columns to avoid conflicts with job_machines columns
    cur.execute("""
        SELECT m.id as machine_id, m.customer_name, m.model, m.serial_number,
               jm.reported_fault, jm.service_notes, jm.status
        FROM machines m
        JOIN job_machines jm ON m.id = jm.machine_id
        WHERE jm.job_id = ?
        ORDER BY jm.id
    """, (job_id,))
    machines = cur.fetchall()
    
    # Also get all machines for this customer for matching parts
    customer_machines = []
    if job:
        cur.execute("""
            SELECT * FROM machines 
            WHERE customer_name = ? 
            ORDER BY serial_number, model
        """, (job["customer_name"],))
        customer_machines = cur.fetchall()
    
    cur.execute("SELECT * FROM parts WHERE job_id = ? ORDER BY id", (job_id,))
    parts = cur.fetchall()
    
    # Calculate travel info
    try:
        travel_under_25 = bool(job["travel_under_25km"] or 0)
    except (KeyError, IndexError):
        travel_under_25 = False
    
    try:
        travel_time_hours = job["travel_time_hours"] or 0
    except (KeyError, IndexError):
        travel_time_hours = 0
    
    print_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    conn.close()
    # Determine if travel was calculated later
    travel_calculated_later = not travel_under_25 and (not travel_time_hours or travel_time_hours == 0)
    
    return render_template(
        "job_export.html",
        job=job,
        contacts=contacts,
        machines=machines,
        customer_machines=customer_machines,
        parts=parts,
        travel_under_25=travel_under_25,
        travel_time_hours=travel_time_hours,
        travel_calculated_later=travel_calculated_later,
        print_date=print_date,
    )


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
