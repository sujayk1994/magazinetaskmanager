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

# Step 3: Clean up old database and migrations
echo "🧹 Cleaning up old database files..."
rm -f magazine_app.db
echo "✅ Cleanup complete"
echo ""

# Step 4: Create database tables directly
echo "🗄️  Creating database tables..."
python << 'PYTHON_SCRIPT'
from app import create_app, db

app = create_app()
with app.app_context():
    db.create_all()
    print("✅ Database tables created successfully!")
PYTHON_SCRIPT
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
