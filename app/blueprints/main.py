from flask import Blueprint, render_template, session, redirect, url_for
from app import db
from app.models import Task, Notification, User, CXOArticle
from app.blueprints.auth import login_required, get_current_user, role_required
from datetime import datetime, timedelta

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    user = get_current_user()
    
    if not user:
        session.clear()
        return redirect(url_for('auth.login'))
    
    todo_tasks = Task.query.filter_by(
        assigned_to_id=user.id
    ).filter(
        Task.status.in_(['Assigned', 'InProgress', 'Review', 'Open'])
    ).order_by(Task.created_at.desc()).limit(5).all()
    
    recent_tasks = Task.query.filter_by(
        assigned_to_id=user.id
    ).order_by(Task.updated_at.desc()).limit(5).all()
    
    upcoming_deadlines = Task.query.filter(
        Task.assigned_to_id == user.id,
        Task.deadline != None,
        Task.deadline >= datetime.utcnow(),
        Task.status.notin_(['Completed', 'Archived'])
    ).order_by(Task.deadline.asc()).limit(10).all()
    
    notifications = Notification.query.filter_by(
        user_id=user.id,
        is_read=False
    ).order_by(Notification.created_at.desc()).limit(5).all()
    
    pending_articles = []
    if user.role == 'editorial' or user.department == 'editorial':
        pending_articles = CXOArticle.query.filter_by(
            status='Pending',
            is_archived=False
        ).order_by(CXOArticle.uploaded_at.desc()).limit(5).all()
    
    open_tasks = []
    design_team = []
    if user.department == 'design':
        open_tasks = Task.query.filter_by(
            assigned_department='design',
            assigned_to_id=None,
            status='Open',
            is_archived=False
        ).order_by(Task.created_at.desc()).all()
    
    if user.department == 'design' and user.is_manager:
        design_team = User.query.filter_by(
            department='design',
            is_manager=False
        ).all()
    
    return render_template('dashboard.html',
                         user=user,
                         todo_tasks=todo_tasks,
                         recent_tasks=recent_tasks,
                         upcoming_deadlines=upcoming_deadlines,
                         notifications=notifications,
                         pending_articles=pending_articles,
                         open_tasks=open_tasks,
                         design_team=design_team)

@bp.route('/cxo-dashboard')
@login_required
@role_required('cxo')
def cxo_dashboard():
    user = get_current_user()
    
    my_articles = CXOArticle.query.filter_by(
        uploaded_by_id=user.id,
        is_archived=False
    ).order_by(CXOArticle.uploaded_at.desc()).all()
    
    pending_articles = CXOArticle.query.filter_by(
        status='Pending',
        is_archived=False
    ).order_by(CXOArticle.uploaded_at.desc()).limit(10).all()
    
    approved_articles = CXOArticle.query.filter_by(
        status='Approved',
        is_used=False,
        is_archived=False
    ).order_by(CXOArticle.uploaded_at.desc()).limit(10).all()
    
    return render_template('cxo_dashboard.html',
                         user=user,
                         my_articles=my_articles,
                         pending_articles=pending_articles,
                         approved_articles=approved_articles)

@bp.route('/notifications/mark-read/<int:notification_id>', methods=['POST'])
@login_required
def mark_notification_read(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    if notification.user_id == session['user_id']:
        notification.is_read = True
        db.session.commit()
    return '', 204

@bp.route('/manager-dashboard')
@login_required
def manager_dashboard():
    user = get_current_user()
    
    if not user.is_manager:
        return redirect(url_for('main.dashboard'))
    
    dept_tasks = Task.query.filter_by(
        assigned_department=user.department,
        is_archived=False
    ).filter(
        Task.status.notin_(['Completed', 'Archived'])
    ).order_by(Task.created_at.desc()).all()
    
    my_team = User.query.filter_by(
        department=user.department,
        is_manager=False
    ).all()
    
    team_workload = []
    for member in my_team:
        active_tasks_count = Task.query.filter_by(
            assigned_to_id=member.id
        ).filter(
            Task.status.notin_(['Completed', 'Archived']),
            Task.is_archived == False
        ).count()
        
        team_workload.append({
            'user': member,
            'active_tasks': active_tasks_count
        })
    
    open_tasks = Task.query.filter_by(
        assigned_department=user.department,
        assigned_to_id=None,
        status='Open',
        is_archived=False
    ).order_by(Task.created_at.desc()).all()
    
    pending_articles = []
    if user.department == 'editorial':
        pending_articles = CXOArticle.query.filter_by(
            assigned_to_id=user.id,
            status='Pending',
            is_archived=False
        ).order_by(CXOArticle.uploaded_at.desc()).all()
    
    stats = {
        'total_department_tasks': len(dept_tasks),
        'open_tasks': len(open_tasks),
        'assigned_tasks': len([t for t in dept_tasks if t.assigned_to_id]),
        'high_priority': len([t for t in dept_tasks if t.priority == 'high']),
        'urgent_priority': len([t for t in dept_tasks if t.priority == 'urgent']),
        'team_members': len(my_team),
        'pending_articles': len(pending_articles)
    }
    
    return render_template('manager_dashboard.html',
                         user=user,
                         dept_tasks=dept_tasks,
                         team_workload=team_workload,
                         open_tasks=open_tasks,
                         pending_articles=pending_articles,
                         stats=stats)
