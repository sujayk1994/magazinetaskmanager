from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, send_file
from app import db
from app.models import Task, Edition, Brand, User, TaskFile, TaskHistory, Notification, CXOArticle
from app.blueprints.auth import login_required, role_required, get_current_user
from werkzeug.utils import secure_filename
import os
from datetime import datetime

bp = Blueprint('tasks', __name__, url_prefix='/tasks')

UPLOAD_FOLDER = 'app/static/uploads/tasks'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'txt', 'mp3', 'wav', 'mp4'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/')
@login_required
def all_tasks():
    user = get_current_user()
    
    search_query = request.args.get('search', '')
    brand_filter = request.args.get('brand', '')
    edition_filter = request.args.get('edition', '')
    status_filter = request.args.get('status', '')
    
    query = Task.query
    
    if search_query:
        query = query.filter(
            (Task.company_name.ilike(f'%{search_query}%')) |
            (Task.description.ilike(f'%{search_query}%'))
        )
    
    if brand_filter:
        query = query.join(Edition).filter(Edition.brand_id == brand_filter)
    
    if edition_filter:
        query = query.filter(Task.edition_id == edition_filter)
    
    if status_filter:
        query = query.filter(Task.status == status_filter)
    
    tasks = query.order_by(Task.created_at.desc()).all()
    brands = Brand.query.all()
    editions = Edition.query.all()
    
    return render_template('tasks/all_tasks.html',
                         user=user,
                         tasks=tasks,
                         brands=brands,
                         editions=editions)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
@role_required('sales', 'manager', 'cxo', 'editorial', 'design')
def create_task():
    user = get_current_user()
    
    if user.role == 'editorial' and not user.is_manager:
        flash('Only editorial managers can create tasks.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    if user.role == 'design' and not user.is_manager:
        flash('Only design managers can create tasks.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        brand_id = request.form.get('brand_id')
        edition_id = request.form.get('edition_id')
        edition_other = request.form.get('edition_other')
        category = request.form.get('category')
        category_other = request.form.get('category_other')
        assigned_department = request.form.get('assigned_department')
        deadline_str = request.form.get('deadline')
        
        if edition_id == 'other':
            edition_id = None
        elif edition_id == 'none':
            edition_id = None
        
        deadline = None
        if deadline_str:
            try:
                deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
            except:
                pass
        
        department_manager = User.query.filter_by(
            department=assigned_department,
            is_manager=True
        ).first()
        
        assigned_to_id = department_manager.id if department_manager else None
        task_status = 'Assigned' if assigned_to_id else 'Open'
        
        original_requester_id = None
        if assigned_department == 'design' and user.department == 'editorial':
            original_requester_id = user.id
        
        task = Task(
            brand_id=int(brand_id) if brand_id else None,
            edition_id=int(edition_id) if edition_id else None,
            edition_other=edition_other if edition_id is None and edition_other else None,
            created_by_id=user.id,
            assigned_to_id=assigned_to_id,
            assigned_department=assigned_department,
            original_requester_id=original_requester_id,
            title=request.form.get('title'),
            category=category,
            category_other=category_other if category == 'Other' else None,
            company_name=request.form.get('company_name'),
            company_url=request.form.get('company_url'),
            description=request.form.get('description'),
            deadline=deadline,
            priority=request.form.get('priority', 'normal'),
            status=task_status,
            current_department=assigned_department
        )
        
        db.session.add(task)
        db.session.flush()
        
        history = TaskHistory(
            task_id=task.id,
            user_id=user.id,
            action='Task Created',
            old_value=None,
            new_value=task_status,
            comment=request.form.get('comments', '')
        )
        db.session.add(history)
        db.session.flush()
        
        if 'files' in request.files:
            files = request.files.getlist('files')
            for file in files:
                if file and file.filename and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    unique_filename = f"{task.id}_{datetime.utcnow().timestamp()}_{filename}"
                    filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
                    
                    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                    file.save(filepath)
                    
                    task_file = TaskFile(
                        task_id=task.id,
                        uploaded_by_id=user.id,
                        history_id=history.id,
                        filename=unique_filename,
                        original_filename=filename,
                        file_path=filepath,
                        file_type=filename.rsplit('.', 1)[1].lower()
                    )
                    db.session.add(task_file)
        
        if assigned_to_id:
            dept_name = assigned_department.capitalize()
            notification = Notification(
                user_id=assigned_to_id,
                task_id=task.id,
                message=f'New task for {dept_name} department assigned by {user.username}'
            )
            db.session.add(notification)
        
        db.session.commit()
        flash('Task created successfully!', 'success')
        return redirect(url_for('tasks.task_detail', task_id=task.id))
    
    brands = Brand.query.all()
    editions = Edition.query.order_by(Edition.created_at.desc()).all()
    editorial_users = User.query.filter_by(role='editorial').all()
    design_users = User.query.filter_by(role='design').all()
    
    categories = ['Profile', 'Article', 'Cover', 'COY Cover', 'COY', 'AD', 'Other']
    
    return render_template('tasks/create_task.html',
                         user=user,
                         brands=brands,
                         editions=editions,
                         editorial_users=editorial_users,
                         design_users=design_users,
                         categories=categories)

@bp.route('/<int:task_id>')
@login_required
def task_detail(task_id):
    user = get_current_user()
    task = Task.query.get_or_404(task_id)
    
    history = TaskHistory.query.filter_by(task_id=task_id).order_by(TaskHistory.created_at.desc()).all()
    files = TaskFile.query.filter_by(task_id=task_id, is_deleted=False).order_by(TaskFile.uploaded_at.desc()).all()
    
    editorial_users = User.query.filter_by(role='editorial').all()
    design_users = User.query.filter_by(role='design').all()
    sales_users = User.query.filter_by(role='sales').all()
    
    return render_template('tasks/task_detail.html',
                         user=user,
                         task=task,
                         history=history,
                         files=files,
                         editorial_users=editorial_users,
                         design_users=design_users,
                         sales_users=sales_users)

@bp.route('/<int:task_id>/upload', methods=['POST'])
@login_required
def upload_files(task_id):
    user = get_current_user()
    task = Task.query.get_or_404(task_id)
    
    if user.role not in ['manager', 'super_admin'] and task.assigned_to_id != user.id and user.role != task.current_department:
        flash('You can only upload files to tasks assigned to you or in your department.', 'danger')
        return redirect(url_for('tasks.task_detail', task_id=task_id))
    
    comment = request.form.get('comment', '')
    file_names = []
    uploaded_files = []
    
    if 'files' in request.files:
        files = request.files.getlist('files')
        
        history = TaskHistory(
            task_id=task.id,
            user_id=user.id,
            action='Files Uploaded',
            old_value=None,
            new_value=None,
            comment=comment
        )
        db.session.add(history)
        db.session.flush()
        
        for file in files:
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_filename = f"{task.id}_{datetime.utcnow().timestamp()}_{filename}"
                filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
                
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                file.save(filepath)
                
                task_file = TaskFile(
                    task_id=task.id,
                    uploaded_by_id=user.id,
                    history_id=history.id,
                    filename=unique_filename,
                    original_filename=filename,
                    file_path=filepath,
                    file_type=filename.rsplit('.', 1)[1].lower()
                )
                db.session.add(task_file)
                file_names.append(filename)
        
        history.new_value = ', '.join(file_names) if file_names else None
    
    db.session.commit()
    flash('Files uploaded successfully!', 'success')
    return redirect(url_for('tasks.task_detail', task_id=task_id))

@bp.route('/<int:task_id>/reassign', methods=['POST'])
@login_required
def reassign_task(task_id):
    user = get_current_user()
    task = Task.query.get_or_404(task_id)
    
    if user.role not in ['manager', 'super_admin', task.current_department]:
        flash('You can only reassign tasks in your department or if you are a manager.', 'danger')
        return redirect(url_for('tasks.task_detail', task_id=task_id))
    
    if task.status == 'Completed':
        flash('Cannot reassign a completed task.', 'warning')
        return redirect(url_for('tasks.task_detail', task_id=task_id))
    
    new_assignee_id = request.form.get('assigned_to')
    new_department = request.form.get('department')
    comment = request.form.get('comment', '')
    
    if new_department not in ['sales', 'editorial', 'design']:
        flash('Invalid department selected.', 'danger')
        return redirect(url_for('tasks.task_detail', task_id=task_id))
    
    if new_assignee_id:
        new_assignee = User.query.get(new_assignee_id)
        if not new_assignee:
            flash('Selected user does not exist.', 'danger')
            return redirect(url_for('tasks.task_detail', task_id=task_id))
    
    old_department = task.current_department
    old_assignee = task.assigned_user.username if task.assigned_user else 'Unassigned'
    
    task.assigned_to_id = new_assignee_id if new_assignee_id else None
    task.assigned_department = new_department
    task.current_department = new_department
    task.updated_at = datetime.utcnow()
    
    if new_department == 'design' and old_department == 'editorial' and not task.original_requester_id:
        if task.assigned_user and task.assigned_user.department == 'editorial':
            task.original_requester_id = task.assigned_to_id
        elif user.department == 'editorial':
            task.original_requester_id = user.id
    
    new_assignee_name = User.query.get(new_assignee_id).username if new_assignee_id else 'Unassigned'
    action_text = f'Task Reassigned'
    
    history = TaskHistory(
        task_id=task.id,
        user_id=user.id,
        action=action_text,
        old_value=f'{old_assignee} ({old_department})',
        new_value=f'{new_assignee_name} ({new_department})',
        from_department=old_department,
        to_department=new_department,
        comment=comment
    )
    db.session.add(history)
    
    if new_assignee_id:
        dept_name = new_department.capitalize() if new_department else 'Unknown'
        notification = Notification(
            user_id=new_assignee_id,
            task_id=task.id,
            message=f'Task reassigned to you by {user.username} ({dept_name} department)'
        )
        db.session.add(notification)
    elif new_department and not new_assignee_id:
        dept_manager = User.query.filter_by(
            department=new_department,
            is_manager=True
        ).first()
        if dept_manager:
            task.assigned_to_id = dept_manager.id
            notification = Notification(
                user_id=dept_manager.id,
                task_id=task.id,
                message=f'New task for {new_department.capitalize()} department from {user.username}'
            )
            db.session.add(notification)
    
    cxo_article = CXOArticle.query.filter_by(task_id=task.id).first()
    if cxo_article:
        cxo_article.sync_with_task()
    
    db.session.commit()
    flash('Task reassigned successfully!', 'success')
    return redirect(url_for('tasks.task_detail', task_id=task_id))

@bp.route('/<int:task_id>/complete', methods=['POST'])
@login_required
def complete_task(task_id):
    user = get_current_user()
    task = Task.query.get_or_404(task_id)
    
    old_status = task.status
    comment = request.form.get('comment', '')
    
    should_return_to_editorial = (
        task.current_department == 'design' and 
        task.original_requester_id and 
        not user.is_manager
    )
    
    if should_return_to_editorial:
        task.status = 'Review'
        task.assigned_to_id = task.original_requester_id
        task.assigned_department = 'editorial'
        task.current_department = 'editorial'
        task.updated_at = datetime.utcnow()
        
        history = TaskHistory(
            task_id=task.id,
            user_id=user.id,
            action='Design Completed - Returned to Editorial',
            old_value=old_status,
            new_value='Review',
            from_department='design',
            to_department='editorial',
            comment=comment
        )
        db.session.add(history)
        
        notification = Notification(
            user_id=task.original_requester_id,
            task_id=task.id,
            message=f'Design work completed by {user.username}. Task returned for your review.'
        )
        db.session.add(notification)
        
        cxo_article = CXOArticle.query.filter_by(task_id=task.id).first()
        if cxo_article:
            cxo_article.sync_with_task()
        
        db.session.commit()
        flash('Design work completed! Task returned to editorial for review.', 'success')
    else:
        task.status = 'Completed'
        task.completed_at = datetime.utcnow()
        task.updated_at = datetime.utcnow()
        
        history = TaskHistory(
            task_id=task.id,
            user_id=user.id,
            action='Task Completed',
            old_value=old_status,
            new_value='Completed',
            comment=comment
        )
        db.session.add(history)
        
        cxo_article = CXOArticle.query.filter_by(task_id=task.id).first()
        if cxo_article:
            cxo_article.sync_with_task()
        
        db.session.commit()
        flash('Task marked as completed!', 'success')
    
    return redirect(url_for('tasks.task_detail', task_id=task_id))

@bp.route('/download/<int:file_id>')
@login_required
def download_file(file_id):
    user = get_current_user()
    task_file = TaskFile.query.get_or_404(file_id)
    task = task_file.task
    
    if user.role not in ['manager', 'super_admin']:
        if task.created_by_id != user.id and task.assigned_to_id != user.id and user.role != task.current_department:
            flash('You do not have permission to download this file.', 'danger')
            return redirect(url_for('tasks.all_tasks'))
    
    return send_file(task_file.file_path, as_attachment=True, download_name=task_file.original_filename)

@bp.route('/delete-file/<int:file_id>', methods=['POST'])
@login_required
def delete_file(file_id):
    user = get_current_user()
    task_file = TaskFile.query.get_or_404(file_id)
    task = task_file.task
    
    if user.role != 'super_admin':
        flash('Only Super Admin can delete files.', 'danger')
        return redirect(url_for('tasks.task_detail', task_id=task.id))
    
    if task_file.is_deleted:
        flash('This file has already been deleted.', 'warning')
        return redirect(url_for('tasks.task_detail', task_id=task.id))
    
    task_file.is_deleted = True
    task_file.deleted_at = datetime.utcnow()
    
    history = TaskHistory(
        task_id=task.id,
        user_id=user.id,
        action='File Deleted',
        old_value=task_file.original_filename,
        new_value=None,
        comment=request.form.get('comment', 'File deleted by Super Admin')
    )
    db.session.add(history)
    
    db.session.commit()
    flash(f'File "{task_file.original_filename}" deleted successfully!', 'success')
    return redirect(url_for('tasks.task_detail', task_id=task.id))

@bp.route('/<int:task_id>/pickup', methods=['POST'])
@login_required
@role_required('editorial', 'design')
def pickup_task(task_id):
    user = get_current_user()
    task = Task.query.get_or_404(task_id)
    
    if task.status != 'Open':
        flash('This task is not available for pickup.', 'warning')
        return redirect(url_for('tasks.task_detail', task_id=task_id))
    
    if task.assigned_to_id is not None:
        flash('This task is already assigned.', 'warning')
        return redirect(url_for('tasks.task_detail', task_id=task_id))
    
    if not user.department:
        flash('You must have a department assigned to pick up tasks.', 'danger')
        return redirect(url_for('tasks.task_detail', task_id=task_id))
    
    if task.current_department != user.department:
        flash('You can only pick up tasks in your department.', 'danger')
        return redirect(url_for('tasks.task_detail', task_id=task_id))
    
    task.assigned_to_id = user.id
    task.status = 'Assigned'
    task.updated_at = datetime.utcnow()
    
    history = TaskHistory(
        task_id=task.id,
        user_id=user.id,
        action='Task Picked Up',
        old_value='Open',
        new_value='Assigned',
        comment=f'Task picked up by {user.username}'
    )
    db.session.add(history)
    
    cxo_article = CXOArticle.query.filter_by(task_id=task.id).first()
    if cxo_article:
        cxo_article.sync_with_task()
    
    db.session.commit()
    flash(f'Task #{task.id} picked up successfully!', 'success')
    
    return redirect(request.referrer or url_for('tasks.my_tasks'))

@bp.route('/<int:task_id>/assign_to_member', methods=['POST'])
@login_required
def assign_to_member(task_id):
    user = get_current_user()
    task = Task.query.get_or_404(task_id)
    
    if not user.is_manager or user.department != task.current_department:
        flash('Only managers can assign tasks to team members.', 'danger')
        return redirect(request.referrer or url_for('main.dashboard'))
    
    if task.status not in ['Open', 'Assigned']:
        flash('This task cannot be reassigned at this time.', 'warning')
        return redirect(request.referrer or url_for('main.dashboard'))
    
    member_id = request.form.get('member_id')
    if not member_id:
        flash('Please select a team member.', 'danger')
        return redirect(request.referrer or url_for('main.dashboard'))
    
    member = User.query.get(member_id)
    if not member or member.department != user.department:
        flash('Invalid team member selected.', 'danger')
        return redirect(request.referrer or url_for('main.dashboard'))
    
    old_assignee = task.assigned_user.username if task.assigned_user else 'Unassigned'
    
    task.assigned_to_id = member.id
    task.status = 'Assigned'
    task.updated_at = datetime.utcnow()
    
    if task.current_department == 'editorial':
        old_owner = task.editorial_owner.username if task.editorial_owner else 'None'
        task.editorial_owner_id = member.id
        new_owner = member.username
        ownership_note = f' [Owner changed: {old_owner} → {new_owner}]' if old_owner != 'None' else f' [Owner set: {new_owner}]'
    elif task.current_department == 'design':
        old_owner = task.design_owner.username if task.design_owner else 'None'
        task.design_owner_id = member.id
        new_owner = member.username
        ownership_note = f' [Owner changed: {old_owner} → {new_owner}]' if old_owner != 'None' else f' [Owner set: {new_owner}]'
    else:
        ownership_note = ''
    
    history = TaskHistory(
        task_id=task.id,
        user_id=user.id,
        action='Task Assigned by Manager',
        old_value=old_assignee,
        new_value=member.username + ownership_note,
        comment=f'Manager assigned task to {member.username}'
    )
    db.session.add(history)
    
    notification = Notification(
        user_id=member.id,
        task_id=task.id,
        message=f'Task #{task.id} assigned to you by {user.username}'
    )
    db.session.add(notification)
    
    cxo_article = CXOArticle.query.filter_by(task_id=task.id).first()
    if cxo_article:
        cxo_article.sync_with_task()
    
    db.session.commit()
    flash(f'Task #{task.id} assigned to {member.username}!', 'success')
    
    return redirect(request.referrer or url_for('main.dashboard'))

@bp.route('/<int:task_id>/send_back_to_manager', methods=['POST'])
@login_required
def send_back_to_manager(task_id):
    user = get_current_user()
    task = Task.query.get_or_404(task_id)
    comment = request.form.get('comment', '').strip()
    
    if user.role not in ['editorial', 'design']:
        flash('Only editorial and design users can use this option.', 'danger')
        return redirect(url_for('tasks.task_detail', task_id=task_id))
    
    if task.assigned_to_id != user.id and not user.is_manager:
        flash('You can only send back tasks that are assigned to you.', 'danger')
        return redirect(url_for('tasks.task_detail', task_id=task_id))
    
    if task.status == 'Completed':
        flash('Cannot reassign a completed task.', 'warning')
        return redirect(url_for('tasks.task_detail', task_id=task_id))
    
    manager = User.query.filter_by(
        department=task.current_department,
        is_manager=True
    ).first()
    
    if not manager:
        flash('No manager found for this department.', 'danger')
        return redirect(url_for('tasks.task_detail', task_id=task_id))
    
    old_assignee = task.assigned_user.username if task.assigned_user else 'Unassigned'
    
    task.assigned_to_id = manager.id
    task.status = 'Assigned'
    task.updated_at = datetime.utcnow()
    
    history = TaskHistory(
        task_id=task.id,
        user_id=user.id,
        action='Sent Back to Manager',
        old_value=old_assignee,
        new_value=manager.username,
        comment=comment or f'Sent back to {manager.username} for review'
    )
    db.session.add(history)
    
    notification = Notification(
        user_id=manager.id,
        task_id=task.id,
        message=f'Task #{task.id} sent back to you for review by {user.username}',
        is_read=False
    )
    db.session.add(notification)
    
    cxo_article = CXOArticle.query.filter_by(task_id=task.id).first()
    if cxo_article:
        cxo_article.sync_with_task()
    
    db.session.commit()
    flash(f'Task sent back to {manager.username} for review!', 'success')
    return redirect(url_for('tasks.my_tasks'))

@bp.route('/<int:task_id>/send_back_to_editor', methods=['POST'])
@login_required
def send_back_to_editor(task_id):
    user = get_current_user()
    task = Task.query.get_or_404(task_id)
    comment = request.form.get('comment', '').strip()
    
    if user.role not in ['editorial', 'design']:
        flash('Only editorial and design users can use this option.', 'danger')
        return redirect(url_for('tasks.task_detail', task_id=task_id))
    
    if task.assigned_to_id != user.id and not user.is_manager:
        flash('You can only send back tasks that are assigned to you.', 'danger')
        return redirect(url_for('tasks.task_detail', task_id=task_id))
    
    if task.status == 'Completed':
        flash('Task is already completed.', 'warning')
        return redirect(url_for('tasks.task_detail', task_id=task_id))
    
    if task.current_department == 'design':
        # Find an editorial user in priority order
        next_user = None
        if task.original_requester and task.original_requester.department == 'editorial':
            next_user = task.original_requester
        elif task.editorial_owner_id:
            next_user = task.editorial_owner
        elif task.creator and task.creator.department == 'editorial':
            next_user = task.creator
        else:
            # Find editorial manager
            editorial_manager = User.query.filter_by(
                department='editorial',
                is_manager=True
            ).first()
            if editorial_manager:
                next_user = editorial_manager
            else:
                # Any editorial team member
                next_user = User.query.filter_by(department='editorial').first()
        
        next_dept = 'editorial'
        
        old_assignee = task.assigned_user.username if task.assigned_user else 'Unassigned'
        task.assigned_to_id = next_user.id if next_user else None
        task.current_department = next_dept
        task.status = 'Assigned' if next_user else 'Open'
        task.updated_at = datetime.utcnow()
        
        history = TaskHistory(
            task_id=task.id,
            user_id=user.id,
            action='Design Completed - Sent to Editorial',
            old_value=old_assignee,
            new_value=next_user.username if next_user else 'Unassigned',
            from_department='design',
            to_department=next_dept,
            comment=comment or 'Design work completed, sending back to editor'
        )
        db.session.add(history)
        
        if next_user:
            notification = Notification(
                user_id=next_user.id,
                task_id=task.id,
                message=f'Task #{task.id} design completed - returned to you by {user.username}',
                is_read=False
            )
            db.session.add(notification)
        
        cxo_article = CXOArticle.query.filter_by(task_id=task.id).first()
        if cxo_article:
            cxo_article.sync_with_task()
        
        db.session.commit()
        flash(f'Task sent back to {next_user.username if next_user else "editorial"}!', 'success')
    
    elif task.current_department == 'editorial':
        if task.design_owner_id:
            next_user = task.design_owner
        else:
            design_manager = User.query.filter_by(
                department='design',
                is_manager=True
            ).first()
            next_user = design_manager
        
        old_assignee = task.assigned_user.username if task.assigned_user else 'Unassigned'
        task.assigned_to_id = next_user.id if next_user else None
        task.current_department = 'design'
        task.status = 'Assigned' if next_user else 'Open'
        task.updated_at = datetime.utcnow()
        
        if not task.original_requester_id:
            task.original_requester_id = user.id
        
        history = TaskHistory(
            task_id=task.id,
            user_id=user.id,
            action='Editorial Completed - Sent to Design',
            old_value=old_assignee,
            new_value=next_user.username if next_user else 'Unassigned',
            from_department='editorial',
            to_department='design',
            comment=comment or 'Editorial work completed, sending to design'
        )
        db.session.add(history)
        
        if next_user:
            notification = Notification(
                user_id=next_user.id,
                task_id=task.id,
                message=f'Task #{task.id} sent to you for design by {user.username}',
                is_read=False
            )
            db.session.add(notification)
        
        cxo_article = CXOArticle.query.filter_by(task_id=task.id).first()
        if cxo_article:
            cxo_article.sync_with_task()
        
        db.session.commit()
        flash(f'Task sent to {next_user.username if next_user else "design team"}!', 'success')
    else:
        flash('Invalid department for this action.', 'danger')
        return redirect(url_for('tasks.task_detail', task_id=task_id))
    
    return redirect(url_for('tasks.my_tasks'))

@bp.route('/<int:task_id>/send_to_sales', methods=['POST'])
@login_required
def send_to_sales(task_id):
    user = get_current_user()
    task = Task.query.get_or_404(task_id)
    comment = request.form.get('comment', '').strip()
    
    if user.role != 'editorial':
        flash('Only editorial users can send tasks to sales.', 'danger')
        return redirect(url_for('tasks.task_detail', task_id=task_id))
    
    if task.assigned_to_id != user.id and not user.is_manager:
        flash('You can only send back tasks that are assigned to you.', 'danger')
        return redirect(url_for('tasks.task_detail', task_id=task_id))
    
    if task.status == 'Completed':
        flash('Cannot reassign a completed task.', 'warning')
        return redirect(url_for('tasks.task_detail', task_id=task_id))
    
    sales_person = task.creator
    if not sales_person or sales_person.department != 'sales':
        flash('No sales person found for this task.', 'danger')
        return redirect(url_for('tasks.task_detail', task_id=task_id))
    
    old_assignee = task.assigned_user.username if task.assigned_user else 'Unassigned'
    
    task.assigned_to_id = sales_person.id
    task.assigned_department = 'sales'
    task.current_department = 'sales'
    task.status = 'Assigned'
    task.updated_at = datetime.utcnow()
    
    history = TaskHistory(
        task_id=task.id,
        user_id=user.id,
        action='Sent to Sales for Client Feedback',
        old_value=old_assignee,
        new_value=sales_person.username,
        from_department='editorial',
        to_department='sales',
        comment=comment or 'Sent back to sales for client feedback'
    )
    db.session.add(history)
    
    notification = Notification(
        user_id=sales_person.id,
        task_id=task.id,
        message=f'Task #{task.id} sent back to you for client feedback by {user.username}',
        is_read=False
    )
    db.session.add(notification)
    
    cxo_article = CXOArticle.query.filter_by(task_id=task.id).first()
    if cxo_article:
        cxo_article.sync_with_task()
    
    db.session.commit()
    flash(f'Task sent to {sales_person.username} for client feedback!', 'success')
    return redirect(url_for('tasks.my_tasks'))

@bp.route('/<int:task_id>/assign_to_team', methods=['POST'])
@login_required
def assign_to_team(task_id):
    user = get_current_user()
    task = Task.query.get_or_404(task_id)
    
    if not user.is_manager and user.role != 'super_admin':
        flash('Only managers can assign tasks to the team.', 'danger')
        return redirect(url_for('tasks.task_detail', task_id=task_id))
    
    if user.department != task.current_department and user.role != 'super_admin':
        flash('You can only assign tasks to your own department team.', 'danger')
        return redirect(url_for('tasks.task_detail', task_id=task_id))
    
    if task.status == 'Completed':
        flash('Cannot reassign a completed task.', 'warning')
        return redirect(url_for('tasks.task_detail', task_id=task_id))
    
    if task.assigned_to_id is None:
        flash('This task is already assigned to the team (unassigned individual).', 'info')
        return redirect(request.referrer or url_for('tasks.all_tasks'))
    
    old_assignee = task.assigned_user.username if task.assigned_user else 'Unassigned'
    old_status = task.status
    
    task.assigned_to_id = None
    task.status = 'Open'
    task.updated_at = datetime.utcnow()
    
    history = TaskHistory(
        task_id=task.id,
        user_id=user.id,
        action='Task Assigned to Team',
        old_value=f'{old_assignee} ({old_status})',
        new_value=f'{task.current_department} team (Open)',
        comment='Task made available to team'
    )
    db.session.add(history)
    
    cxo_article = CXOArticle.query.filter_by(task_id=task.id).first()
    if cxo_article:
        cxo_article.sync_with_task()
    
    db.session.commit()
    flash(f'Task #{task.id} assigned to {task.current_department} team!', 'success')
    
    return redirect(request.referrer or url_for('tasks.all_tasks'))

@bp.route('/my-tasks')
@login_required
def my_tasks():
    user = get_current_user()
    
    search_query = request.args.get('search', '')
    status_filter = request.args.get('status', '')
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    query = Task.query.filter_by(assigned_to_id=user.id)
    
    if search_query:
        query = query.filter(
            (Task.company_name.ilike(f'%{search_query}%')) |
            (Task.description.ilike(f'%{search_query}%'))
        )
    
    if status_filter:
        query = query.filter(Task.status == status_filter)
    
    pagination = query.order_by(Task.deadline.asc().nullslast(), Task.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('tasks/my_tasks.html',
                         user=user,
                         tasks=pagination.items,
                         pagination=pagination)

@bp.route('/open-tasks')
@login_required
def open_tasks():
    user = get_current_user()
    
    search_query = request.args.get('search', '')
    brand_filter = request.args.get('brand', '')
    department_filter = request.args.get('department', '')
    priority_filter = request.args.get('priority', '')
    
    query = Task.query.filter(Task.status == 'Open', Task.assigned_to_id.is_(None))
    
    if search_query:
        query = query.filter(
            (Task.company_name.ilike(f'%{search_query}%')) |
            (Task.description.ilike(f'%{search_query}%'))
        )
    
    if brand_filter:
        query = query.filter(Task.brand_id == brand_filter)
    
    if department_filter:
        query = query.filter(Task.current_department == department_filter)
    
    if priority_filter:
        query = query.filter(Task.priority == priority_filter)
    
    tasks = query.order_by(Task.created_at.desc()).all()
    brands = Brand.query.all()
    
    return render_template('tasks/open_tasks.html',
                         user=user,
                         tasks=tasks,
                         brands=brands)
