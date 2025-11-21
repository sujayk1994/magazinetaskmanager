# Magazine Task Management System - Commands Reference

This document provides a comprehensive guide to all available scripts and commands for managing the Magazine Task Management System.

---

## 🚀 Quick Start

### Start the Application
Run the entire application with a single command:
```bash
./startup.sh
```

**What it does:**
- Installs all Python dependencies
- Creates upload directories
- Initializes and runs database migrations
- Seeds the database with sample data (if empty)
- Cleans up any existing Flask instances
- Starts the Flask application on port 5000

**Access the application at:** http://0.0.0.0:5000

---

## 📋 Available Scripts

### 1. Startup Script
**File:** `startup.sh`

**Command:**
```bash
./startup.sh
```

**Description:**
Complete setup and startup script. This is the recommended way to run the application.

**Features:**
- Idempotent (safe to run multiple times)
- Auto-detects if database needs seeding
- Handles port conflicts automatically
- Shows login credentials on startup

---

### 2. Seed Database with Sample Data
**File:** `seed_comprehensive_with_managers.py`

**Command:**
```bash
python seed_comprehensive_with_managers.py
```

**Description:**
Seeds the database with comprehensive sample data for testing and demonstration.

**Creates:**
- 14 users (including department managers)
- 5 brands
- 30 editions
- 28 tasks (demonstrating various workflows)
- 10 CXO articles
- Sample notifications and task history

**Sample Users Created:**
| Username | Role | Department | Manager | Password |
|----------|------|------------|---------|----------|
| super_admin | Super Admin | admin | Yes | password123 |
| ceo_john | CXO | executive | Yes | password123 |
| cmo_sarah | CXO | executive | No | password123 |
| sales_manager | Sales | sales | Yes | password123 |
| john_sales | Sales | sales | No | password123 |
| mary_sales | Sales | sales | No | password123 |
| editorial_manager | Editorial | editorial | Yes | password123 |
| editor_jane | Editorial | editorial | No | password123 |
| editor_mike | Editorial | editorial | No | password123 |
| editor_lisa | Editorial | editorial | No | password123 |
| design_manager | Design | design | Yes | password123 |
| designer_sarah | Design | design | No | password123 |
| designer_david | Design | design | No | password123 |
| designer_amy | Design | design | No | password123 |

**Warning:** This script clears all existing data before seeding!

---

### 3. Clear Content Data
**File:** `clear_content.py`

**Command:**
```bash
python clear_content.py
```

**Description:**
Interactive cleanup utility with two modes for clearing content data while preserving user accounts.

**Mode 1: Clear Tasks Only (Recommended)**
- **Deletes:** Tasks, Task Files, Task History, CXO Articles, Ads, Notifications
- **Preserves:** Users, Brands, Editions
- **Result:** Clean slate for tasks, but brands/editions remain for creating new work
- **Use Case:** Clean up old tasks while keeping reference data

**Mode 2: Clear All Content**
- **Deletes:** Everything except users (brands, editions, tasks, files, articles, ads, notifications)
- **Preserves:** Only users and authentication data
- **Result:** Completely empty database
- **Use Case:** Complete reset (requires re-seeding or manual brand/edition creation)
- **Warning:** App cannot create tasks until brands/editions are added back

**Interactive Features:**
- Menu-driven interface
- Confirmation prompts before deletion
- Clear warnings about what will be deleted
- Status summary after completion

---

### 4. Run Main Application
**File:** `main.py`

**Command:**
```bash
python main.py
```

**Description:**
Directly runs the Flask application without setup steps.

**Note:** Only use this if dependencies are already installed and database is set up. Otherwise, use `./startup.sh`.

---

## 🗄️ Database Management

### Initialize Database Migrations
```bash
flask db init
```
Creates the migrations directory. Only needed once.

### Create a New Migration
```bash
flask db migrate -m "Description of changes"
```
Generates a new migration file based on model changes.

### Apply Migrations
```bash
flask db upgrade
```
Applies all pending migrations to the database.

### Rollback Migration
```bash
flask db downgrade
```
Rolls back the last migration.

### Check Current Migration Version
```bash
flask db current
```
Shows the current migration version.

### View Migration History
```bash
flask db history
```
Shows all migrations in order.

---

## 🛠️ Development Commands

### Install Dependencies
```bash
uv pip install -r <(python -c "import sys; print('\n'.join([
    'flask>=3.1.2',
    'flask-dance>=7.1.0',
    'flask-login>=0.6.3',
    'flask-migrate>=4.1.0',
    'flask-sqlalchemy>=3.1.1',
    'flask-wtf>=1.2.2',
    'oauthlib>=3.3.1',
    'psycopg2-binary>=2.9.11',
    'pyjwt>=2.10.1',
    'python-dotenv>=1.2.1'
]))")
```

### Create Upload Directories
```bash
mkdir -p app/static/uploads/tasks
mkdir -p app/static/uploads/ads
mkdir -p app/static/uploads/cxo_articles
```

### Clean Up Running Instances
```bash
pkill -f "python main.py"
```

---

## 📝 Common Workflows

### First Time Setup
```bash
./startup.sh
```
That's it! The script handles everything.

### Clear Tasks and Keep Working (Recommended)
```bash
# Option 1: Clear tasks only (keeps brands/editions)
python clear_content.py
# Choose option 1 when prompted

# You can now create new tasks using existing brands/editions
```

### Start Fresh with New Sample Data
```bash
# Option 1: Clear everything then re-seed
python clear_content.py
# Choose option 2 when prompted (clears brands/editions too)

# Re-seed with sample data
python seed_comprehensive_with_managers.py

# Option 2: Just clear tasks and manually add content
python clear_content.py
# Choose option 1 when prompted (keeps brands/editions)
# Then manually create tasks through the UI
```

### Complete Database Reset
```bash
# Stop the application
pkill -f "python main.py"

# Delete the database file (SQLite)
rm -f magazine_app.db

# Or drop all tables (PostgreSQL)
flask shell
>>> from app import db
>>> db.drop_all()
>>> exit()

# Restart with fresh setup
./startup.sh
```

### Update Database Schema
```bash
# 1. Modify models in app/models.py

# 2. Create migration
flask db migrate -m "Description of changes"

# 3. Review the migration file in migrations/versions/

# 4. Apply migration
flask db upgrade

# 5. Restart application
./startup.sh
```

---

## 🔧 Troubleshooting

### Port Already in Use
If you see "Address already in use" error:
```bash
pkill -f "python main.py"
./startup.sh
```

### Database Migration Issues
```bash
# Stamp database with current version
flask db stamp head

# Then upgrade
flask db upgrade
```

### Reset Everything
```bash
# Delete database
rm -f magazine_app.db

# Delete migrations (optional)
rm -rf migrations

# Start fresh
./startup.sh
```

---

## 📊 Default Login Credentials

All seeded users have the same password: `password123`

### Quick Access Accounts
- **Super Admin:** `super_admin` / `password123`
- **Sales Manager:** `sales_manager` / `password123`
- **Editorial Manager:** `editorial_manager` / `password123`
- **Design Manager:** `design_manager` / `password123`

---

## 📖 File Structure

```
.
├── startup.sh                          # Main startup script
├── clear_content.py                    # Clear content data script
├── seed_comprehensive_with_managers.py # Seed database script
├── main.py                            # Flask application entry point
├── config.py                          # Application configuration
├── app/                               # Application package
│   ├── __init__.py                   # App factory
│   ├── models.py                     # Database models
│   ├── blueprints/                   # Route blueprints
│   ├── templates/                    # HTML templates
│   └── static/                       # Static files (CSS, JS, uploads)
├── migrations/                        # Database migrations
└── COMMANDS.md                        # This file
```

---

## 🎯 Environment Variables

The application uses the following environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `SESSION_SECRET` | `dev-secret-key-change-in-production` | Flask session secret key |
| `DATABASE_URL` | `sqlite:///magazine_app.db` | Database connection string |

**Note:** PostgreSQL is supported. Set `DATABASE_URL` to your PostgreSQL connection string.

---

## 📞 Support

For issues or questions:
1. Check the logs in the Flask console output
2. Review this documentation
3. Check the application documentation in `README.md`
4. Review technical documentation in `TECHNICAL_DOCUMENTATION.md`

---

**Last Updated:** November 21, 2025
