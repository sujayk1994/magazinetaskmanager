#!/bin/bash
# Quick setup and run script - installs, migrates, seeds, and runs the app

echo "🚀 Setting up Magazine Task Management System..."

# Install dependencies
echo "Installing dependencies..."
pip install flask flask-dance flask-login flask-migrate flask-sqlalchemy flask-wtf oauthlib psycopg2-binary pyjwt python-dotenv 2>/dev/null || true

# Create database tables
echo "Creating database..."
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()" 2>/dev/null || true

# Seed database
echo "Seeding database..."
python seed_comprehensive_with_managers.py 2>/dev/null || true

# Run the app
echo "Starting application on http://0.0.0.0:5000"
python main.py
