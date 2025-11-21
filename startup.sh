#!/bin/bash

# Magazine Task Management System - Startup Script
# This script installs dependencies, sets up the database, and runs the application

set -e  # Exit on any error

echo "========================================"
echo "Magazine Task Management System Startup"
echo "========================================"
echo ""

# Step 1: Install Python dependencies
echo "📦 Installing Python dependencies..."
if command -v uv &> /dev/null; then
    # Use uv if available (Replit)
    uv pip install -r requirements.txt
else
    # Use standard pip (GitHub, local, other environments)
    pip install -r requirements.txt
fi
echo "✅ Dependencies installed"
echo ""

# Step 2: Create upload directories if they don't exist
echo "📁 Creating upload directories..."
mkdir -p app/static/uploads/tasks
mkdir -p app/static/uploads/ads
mkdir -p app/static/uploads/cxo_articles
echo "✅ Upload directories ready"
echo ""

# Step 3: Initialize database migrations (if not already initialized)
echo "🗄️  Setting up database migrations..."
if [ ! -d "migrations" ]; then
    echo "Initializing Flask-Migrate..."
    python -m flask db init
fi
echo "✅ Migrations initialized"
echo ""

# Step 4: Run database migrations (idempotent - safe to run multiple times)
echo "📊 Running database migrations..."
python -m flask db upgrade 2>&1 | grep -v "INFO" || true
echo "✅ Database is up to date"
echo ""

# Step 5: Check if database needs seeding
echo "🌱 Checking if database needs seeding..."
NEEDS_SEED=$(python -c "
from app import create_app, db
from app.models import User
app = create_app()
with app.app_context():
    count = User.query.count()
    print('yes' if count == 0 else 'no')
" 2>/dev/null || echo "yes")

if [ "$NEEDS_SEED" = "yes" ]; then
    echo "Database is empty. Seeding with sample data..."
    python seed_comprehensive_with_managers.py
    echo "✅ Database seeded successfully"
else
    USER_COUNT=$(python -c "from app import create_app, db; from app.models import User; app = create_app(); app.app_context().push(); print(User.query.count())" 2>/dev/null || echo "?")
    echo "ℹ️  Database already has data ($USER_COUNT users). Skipping seeding."
    echo "   To reseed, clear the database and run this script again."
fi
echo ""

# Step 6: Clean up any existing Flask instances
echo "🧹 Cleaning up any existing Flask instances..."
pkill -f "python main.py" 2>/dev/null || true
sleep 1
echo "✅ Ready to start"
echo ""

# Step 7: Run the Flask application
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
