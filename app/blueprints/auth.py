from flask import Blueprint, session, redirect, url_for, request, flash, render_template
from app import db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
import os
from functools import wraps

bp = Blueprint('auth', __name__, url_prefix='/auth')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('auth.login'))
            user = User.query.get(session['user_id'])
            if not user:
                flash('User not found.', 'danger')
                return redirect(url_for('auth.login'))
            if user.role == 'super_admin' or user.role in roles:
                return f(*args, **kwargs)
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main.dashboard'))
        return decorated_function
    return decorator

def super_admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        user = User.query.get(session['user_id'])
        if not user or user.role != 'super_admin':
            flash('Super Admin access required.', 'danger')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def get_role_based_redirect(user_role):
    role_redirects = {
        'super_admin': 'main.dashboard',
        'cxo': 'main.cxo_dashboard',
        'sales': 'main.dashboard',
        'editorial': 'main.dashboard',
        'design': 'main.dashboard',
        'manager': 'main.dashboard'
    }
    return url_for(role_redirects.get(user_role, 'main.dashboard'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password', 'password123')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            session.permanent = True
            flash(f'Welcome, {user.username}!', 'success')
            return redirect(get_role_based_redirect(user.role))
        else:
            flash('Invalid username or password. Please try again.', 'danger')
    
    users = User.query.all()
    return render_template('auth/login.html', users=users)

@bp.route('/callback')
def callback():
    user_data = request.headers.get('X-Replit-User-Id')
    username = request.headers.get('X-Replit-User-Name')
    
    if not user_data:
        flash('Authentication failed', 'danger')
        return redirect(url_for('main.index'))
    
    user = User.query.filter_by(replit_user_id=user_data).first()
    
    if not user:
        user = User(
            replit_user_id=user_data,
            username=username or f'user_{user_data[:8]}',
            password=generate_password_hash('password123'),
            role='sales'
        )
        db.session.add(user)
        db.session.commit()
    
    session['user_id'] = user.id
    session['username'] = user.username
    session['role'] = user.role
    session.permanent = True
    
    return redirect(url_for('main.dashboard'))

@bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

def get_current_user():
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None
