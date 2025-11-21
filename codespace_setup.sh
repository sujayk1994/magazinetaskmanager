#!/bin/bash

# GitHub Codespaces Setup Script
# Run this script to set up and start the Magazine Task Management System

set -e

echo "========================================"
echo "GitHub Codespaces Setup"
echo "Magazine Task Management System"
echo "========================================"
echo ""

# Step 1: Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt --quiet
echo "✅ Dependencies installed"
echo ""

# Step 2: Create upload directories
echo "📁 Creating upload directories..."
mkdir -p app/static/uploads/tasks
mkdir -p app/static/uploads/ads
mkdir -p app/static/uploads/cxo_articles
echo "✅ Upload directories ready"
echo ""

# Step 3: Clean up old database, migrations, and Python cache
echo "🧹 Cleaning up old files..."
rm -f magazine_app.db
rm -rf __pycache__
rm -rf app/__pycache__
rm -rf app/blueprints/__pycache__
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
echo "✅ Cleanup complete"
echo ""

# Step 4: Create database tables directly (force fresh import)
echo "🗄️  Creating database tables..."
python -c "
import sys
# Clear any cached imports
if 'app' in sys.modules:
    del sys.modules['app']
if 'app.models' in sys.modules:
    del sys.modules['app.models']

from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    db.create_all()
    
    # Verify password column exists
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    columns = [c['name'] for c in inspector.get_columns('users')]
    
    if 'password' not in columns:
        print('ERROR: password column not created!')
        print('Columns found:', columns)
        exit(1)
    
    print('✅ Database tables created successfully with all columns!')
"
echo ""

# Step 5: Seed the database
echo "🌱 Seeding database with sample data..."
python seed_comprehensive_with_managers.py
echo "✅ Database seeded successfully"
echo ""

# Step 6: Start the application
echo "🚀 Starting Flask application..."
echo "========================================"
echo "Application will be available at:"
echo "  http://0.0.0.0:5000"
echo "========================================"
echo ""
echo "Login credentials:"
echo "  Username: super_admin | Password: password123"
echo "  Username: sales_manager | Password: password123"
echo "  Username: editorial_manager | Password: password123"
echo "  Username: design_manager | Password: password123"
echo "========================================"
echo ""
python main.py
