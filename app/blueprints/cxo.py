from flask import Blueprint, render_template, request, flash, redirect, url_for, session, send_file
from werkzeug.utils import secure_filename
from app import db
from app.models import CXOArticle, CXOArticleFile, Brand, Edition, User, Task, Notification
from app.blueprints.auth import login_required, get_current_user, role_required, super_admin_required
from datetime import datetime
import os

bp = Blueprint('cxo', __name__, url_prefix='/cxo')

UPLOAD_FOLDER = 'app/static/uploads/cxo_articles'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'png', 'jpg', 'jpeg'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/articles')
@login_required
@role_required('sales', 'cxo', 'editorial', 'design', 'super_admin')
def all_articles():
    user = get_current_user()
    
    brand_filter = request.args.get('brand', '')
    edition_filter = request.args.get('edition', '')
    status_filter = request.args.get('status', '')
    
    query = CXOArticle.query
    
    if user.role in ['cxo', 'sales']:
        query = query.filter_by(uploaded_by_id=user.id)
    
    if user.role != 'super_admin':
        query = query.filter_by(is_archived=False)
    
    if brand_filter:
        try:
            query = query.filter(CXOArticle.brand_id == int(brand_filter))
        except ValueError:
            pass
    
    if edition_filter:
        try:
            query = query.filter(CXOArticle.edition_id == int(edition_filter))
        except ValueError:
            pass
    
    if status_filter:
        if status_filter == 'Used':
            query = query.filter(CXOArticle.is_used == True)
        else:
            query = query.filter(CXOArticle.status == status_filter)
    
    articles = query.order_by(CXOArticle.uploaded_at.desc()).all()
    brands = Brand.query.all()
    editions = Edition.query.all()
    statuses = ['Pending', 'Approved', 'Rejected', 'Designing', 'Design Ready', 'Used']
    
    return render_template('cxo/all_articles.html',
                         user=user,
                         articles=articles,
                         brands=brands,
                         editions=editions,
                         statuses=statuses)

@bp.route('/upload-article', methods=['GET', 'POST'])
@login_required
@role_required('sales', 'cxo', 'super_admin')
def upload_article():
    user = get_current_user()
    
    if request.method == 'POST':
        brand_id = request.form.get('brand_id')
        edition_id = request.form.get('edition_id')
        edition_other = request.form.get('edition_other')
        company_name = request.form.get('company_name')
        contact_person_name = request.form.get('contact_person_name')
        contact_person_designation = request.form.get('contact_person_designation')
        company_url = request.form.get('company_url')
        comments = request.form.get('comments')
        override_assign = request.form.get('override_assign')
        assigned_to_id = request.form.get('assigned_to_id')
        
        if not brand_id or not company_name:
            flash('Brand and Company Name are required!', 'danger')
            return redirect(url_for('cxo.upload_article'))
        
        if edition_id == 'other':
            edition_id = None
        elif edition_id:
            edition_id = int(edition_id)
        else:
            edition_id = None
        
        assigned_editor = None
        if override_assign and assigned_to_id:
            assigned_editor = int(assigned_to_id)
        elif user.role == 'sales':
            editorial_manager = User.query.filter_by(
                department='editorial',
                is_manager=True
            ).first()
            if editorial_manager:
                assigned_editor = editorial_manager.id
        
        article = CXOArticle(
            brand_id=int(brand_id),
            edition_id=edition_id,
            edition_other=edition_other if edition_id is None else None,
            company_name=company_name,
            contact_person_name=contact_person_name,
            contact_person_designation=contact_person_designation,
            company_url=company_url,
            comments=comments,
            uploaded_by_id=user.id,
            assigned_to_id=assigned_editor,
            status='Pending'
        )
        
        db.session.add(article)
        db.session.flush()
        
        task = Task(
            brand_id=int(brand_id),
            edition_id=edition_id,
            created_by_id=user.id,
            assigned_to_id=assigned_editor,
            assigned_department='editorial',
            title=f'CXO Article Review: {company_name}',
            category='CXO Article',
            company_name=company_name,
            company_url=company_url,
            description=f'Review and approve CXO article for {company_name}. {comments if comments else ""}',
            priority='normal',
            status='Assigned' if assigned_editor else 'Open',
            current_department='editorial'
        )
        db.session.add(task)
        db.session.flush()
        
        article.task_id = task.id
        
        if user.role == 'sales' and assigned_editor:
            notification = Notification(
                user_id=assigned_editor,
                task_id=task.id,
                message=f'New CXO Article uploaded by {user.username} for {company_name} - requires approval'
            )
            db.session.add(notification)
        
        uploaded_files = []
        if 'files' in request.files:
            files = request.files.getlist('files')
            for file in files:
                if file and file.filename and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
                    unique_filename = f"{article.id}_{timestamp}_{filename}"
                    filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
                    file.save(filepath)
                    
                    article_file = CXOArticleFile(
                        article_id=article.id,
                        original_filename=filename,
                        stored_filename=unique_filename,
                        file_path=filepath,
                        file_type=filename.rsplit('.', 1)[1].lower() if '.' in filename else 'unknown'
                    )
                    db.session.add(article_file)
                    uploaded_files.append(filename)
        
        db.session.commit()
        
        flash(f'Article uploaded successfully with {len(uploaded_files)} file(s)!', 'success')
        return redirect(url_for('cxo.all_articles'))
    
    brands = Brand.query.all()
    editions = Edition.query.all()
    editors = User.query.filter_by(role='editorial').all()
    
    return render_template('cxo/upload_article.html',
                         user=user,
                         brands=brands,
                         editions=editions,
                         editors=editors)

@bp.route('/article/<int:article_id>')
@login_required
@role_required('sales', 'cxo', 'editorial', 'design', 'super_admin')
def article_detail(article_id):
    user = get_current_user()
    article = CXOArticle.query.get_or_404(article_id)
    
    if user.role in ['cxo', 'sales'] and article.uploaded_by_id != user.id:
        flash('You do not have permission to view this article.', 'danger')
        return redirect(url_for('cxo.all_articles'))
    
    editions = Edition.query.all()
    
    return render_template('cxo/article_detail.html',
                         user=user,
                         article=article,
                         editions=editions)

@bp.route('/download/<int:file_id>')
@login_required
@role_required('sales', 'cxo', 'editorial', 'design', 'super_admin')
def download_file(file_id):
    user = get_current_user()
    article_file = CXOArticleFile.query.get_or_404(file_id)
    article = article_file.article
    
    if user.role in ['cxo', 'sales'] and article.uploaded_by_id != user.id:
        flash('You do not have permission to download this file.', 'danger')
        return redirect(url_for('cxo.all_articles'))
    
    return send_file(article_file.file_path, as_attachment=True, download_name=article_file.original_filename)

@bp.route('/article/<int:article_id>/approve', methods=['POST'])
@login_required
@role_required('editorial', 'super_admin')
def approve_article(article_id):
    user = get_current_user()
    article = CXOArticle.query.get_or_404(article_id)
    
    if article.status != 'Pending':
        flash('This article has already been reviewed.', 'warning')
        return redirect(url_for('cxo.article_detail', article_id=article.id))
    
    edition_id = request.form.get('edition_id')
    editor_comments = request.form.get('editor_comments', '')
    create_design_task = request.form.get('create_design_task') == 'on'
    
    old_edition_id = article.edition_id
    if edition_id and edition_id != 'keep' and edition_id != str(article.edition_id):
        article.edition_id = int(edition_id)
    
    article.status = 'Approved'
    article.updated_at = datetime.utcnow()
    
    if article.task:
        article.task.status = 'Completed'
        article.task.updated_at = datetime.utcnow()
        article.sync_with_task()
    
    separator = '\n\n---\n' if article.comments and article.comments.strip() else ''
    approval_note = f'{separator}[APPROVED by {user.username} on {datetime.utcnow().strftime("%Y-%m-%d %H:%M")}]'
    if editor_comments:
        approval_note += f': {editor_comments}'
    if old_edition_id != article.edition_id:
        old_edition = Edition.query.get(old_edition_id) if old_edition_id else None
        new_edition = Edition.query.get(article.edition_id) if article.edition_id else None
        approval_note += f'\nEdition changed from "{old_edition.name if old_edition else "N/A"}" to "{new_edition.name if new_edition else "N/A"}"'
    
    article.comments = (article.comments or '') + approval_note
    
    notification = Notification(
        user_id=article.uploaded_by_id,
        message=f'Your article for {article.company_name} has been approved by {user.username}!',
        is_read=False
    )
    db.session.add(notification)
    
    if create_design_task:
        description_text = f'Design task for approved CXO article #{article.id}'
        if editor_comments:
            description_text += f'\n\nEditor Comments: {editor_comments}'
        
        task = Task(
            brand_id=article.brand_id,
            edition_id=article.edition_id,
            created_by_id=user.id,
            assigned_to_id=None,
            assigned_department='design',
            company_name=article.company_name,
            category='CXO Article',
            current_department='design',
            status='Open',
            description=description_text
        )
        db.session.add(task)
        db.session.flush()
        
        article.task_id = task.id
        article.sync_with_task()
        
        design_users = User.query.filter_by(role='design').all()
        for design_user in design_users:
            design_notification = Notification(
                user_id=design_user.id,
                message=f'New design task #{task.id} created for CXO article: {article.company_name}',
                task_id=task.id,
                is_read=False
            )
            db.session.add(design_notification)
    
    db.session.commit()
    
    flash(f'Article approved successfully! {"Design task created." if create_design_task else ""}', 'success')
    return redirect(url_for('cxo.article_detail', article_id=article.id))

@bp.route('/article/<int:article_id>/reject', methods=['POST'])
@login_required
@role_required('editorial', 'super_admin')
def reject_article(article_id):
    user = get_current_user()
    article = CXOArticle.query.get_or_404(article_id)
    
    if article.status != 'Pending':
        flash('This article has already been reviewed.', 'warning')
        return redirect(url_for('cxo.article_detail', article_id=article.id))
    
    reject_reason = request.form.get('reject_reason', '').strip()
    
    if not reject_reason:
        flash('Please provide a reason for rejection.', 'danger')
        return redirect(url_for('cxo.article_detail', article_id=article.id))
    
    article.status = 'Rejected'
    article.updated_at = datetime.utcnow()
    
    if article.task:
        article.task.status = 'Completed'
        article.task.updated_at = datetime.utcnow()
        article.sync_with_task()
    
    separator = '\n\n---\n' if article.comments and article.comments.strip() else ''
    rejection_note = f'{separator}[REJECTED by {user.username} on {datetime.utcnow().strftime("%Y-%m-%d %H:%M")}]: {reject_reason}'
    article.comments = (article.comments or '') + rejection_note
    
    notification = Notification(
        user_id=article.uploaded_by_id,
        message=f'Your article for {article.company_name} was rejected by {user.username}. Reason: {reject_reason}',
        is_read=False
    )
    db.session.add(notification)
    
    db.session.commit()
    
    flash('Article rejected. The CXO user has been notified.', 'info')
    return redirect(url_for('cxo.article_detail', article_id=article.id))

@bp.route('/article/<int:article_id>/mark-used', methods=['POST'])
@login_required
@role_required('editorial', 'super_admin')
def mark_article_used(article_id):
    user = get_current_user()
    article = CXOArticle.query.get_or_404(article_id)
    
    if article.status != 'Approved':
        flash('Only approved articles can be marked as used.', 'warning')
        return redirect(url_for('cxo.article_detail', article_id=article.id))
    
    if article.is_used:
        flash('This article has already been marked as used.', 'info')
        return redirect(url_for('cxo.article_detail', article_id=article.id))
    
    article.is_used = True
    article.used_at = datetime.utcnow()
    article.updated_at = datetime.utcnow()
    
    separator = '\n\n---\n' if article.comments and article.comments.strip() else ''
    used_note = f'{separator}[MARKED AS USED by {user.username} on {datetime.utcnow().strftime("%Y-%m-%d %H:%M")}]'
    article.comments = (article.comments or '') + used_note
    
    notification = Notification(
        user_id=article.uploaded_by_id,
        message=f'Your article for {article.company_name} has been marked as used in {article.edition.name if article.edition else "the magazine"}!',
        is_read=False
    )
    db.session.add(notification)
    
    db.session.commit()
    
    flash('Article marked as used successfully!', 'success')
    return redirect(url_for('cxo.article_detail', article_id=article.id))

@bp.route('/article/<int:article_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    user = get_current_user()
    article = CXOArticle.query.get_or_404(article_id)
    
    if user.role != 'cxo' or not user.is_manager:
        flash('Only CXO managers can edit articles.', 'danger')
        return redirect(url_for('cxo.article_detail', article_id=article.id))
    
    if article.is_used:
        flash('Cannot edit articles that have already been used.', 'warning')
        return redirect(url_for('cxo.article_detail', article_id=article.id))
    
    if request.method == 'POST':
        brand_id = request.form.get('brand_id')
        edition_id = request.form.get('edition_id')
        edition_other = request.form.get('edition_other')
        company_name = request.form.get('company_name')
        contact_person_name = request.form.get('contact_person_name')
        contact_person_designation = request.form.get('contact_person_designation')
        company_url = request.form.get('company_url')
        assigned_to_id = request.form.get('assigned_to_id')
        
        if not brand_id or not company_name:
            flash('Brand and Company Name are required!', 'danger')
            return redirect(url_for('cxo.edit_article', article_id=article.id))
        
        old_brand = article.brand.name
        old_edition = article.edition.name if article.edition else (article.edition_other or 'N/A')
        old_assignee = article.assigned_to.username if article.assigned_to else 'Unassigned'
        old_company_name = article.company_name
        old_contact_person = article.contact_person_name or 'N/A'
        old_designation = article.contact_person_designation or 'N/A'
        old_url = article.company_url or 'N/A'
        
        article.brand_id = int(brand_id)
        
        if edition_id == 'other':
            article.edition_id = None
            article.edition_other = edition_other
        elif edition_id:
            article.edition_id = int(edition_id)
            article.edition_other = None
        else:
            article.edition_id = None
            article.edition_other = None
        
        article.company_name = company_name
        article.contact_person_name = contact_person_name
        article.contact_person_designation = contact_person_designation
        article.company_url = company_url
        
        if assigned_to_id:
            article.assigned_to_id = int(assigned_to_id)
        else:
            article.assigned_to_id = None
        
        article.updated_at = datetime.utcnow()
        
        new_brand = article.brand.name
        new_edition = article.edition.name if article.edition else (article.edition_other or 'N/A')
        new_assignee = article.assigned_to.username if article.assigned_to else 'Unassigned'
        new_company_name = article.company_name
        new_contact_person = article.contact_person_name or 'N/A'
        new_designation = article.contact_person_designation or 'N/A'
        new_url = article.company_url or 'N/A'
        
        changes = []
        if old_brand != new_brand:
            changes.append(f'Brand: {old_brand} → {new_brand}')
        if old_edition != new_edition:
            changes.append(f'Edition: {old_edition} → {new_edition}')
        if old_assignee != new_assignee:
            changes.append(f'Assigned to: {old_assignee} → {new_assignee}')
        if old_company_name != new_company_name:
            changes.append(f'Company Name: {old_company_name} → {new_company_name}')
        if old_contact_person != new_contact_person:
            changes.append(f'Contact Person: {old_contact_person} → {new_contact_person}')
        if old_designation != new_designation:
            changes.append(f'Designation: {old_designation} → {new_designation}')
        if old_url != new_url:
            changes.append(f'Company URL: {old_url} → {new_url}')
        
        if changes:
            separator = '\n\n---\n' if article.comments and article.comments.strip() else ''
            edit_note = f'{separator}[EDITED by {user.username} on {datetime.utcnow().strftime("%Y-%m-%d %H:%M")}]\nChanges: {", ".join(changes)}'
            article.comments = (article.comments or '') + edit_note
        
        was_rejected = article.status == 'Rejected'
        if was_rejected:
            article.status = 'Approved'
            
            approval_note = f'\n[AUTO-APPROVED after edit by {user.username} on {datetime.utcnow().strftime("%Y-%m-%d %H:%M")}]'
            article.comments = (article.comments or '') + approval_note
            
            design_task = Task(
                brand_id=article.brand_id,
                edition_id=article.edition_id,
                created_by_id=user.id,
                assigned_to_id=None,
                assigned_department='design',
                company_name=article.company_name,
                category='CXO Article',
                current_department='design',
                status='Open',
                description=f'Design task for re-approved CXO article #{article.id}',
                title=f'CXO Article Design: {article.company_name}'
            )
            db.session.add(design_task)
            db.session.flush()
            
            article.task_id = design_task.id
            article.sync_with_task()
            
            design_users = User.query.filter_by(role='design').all()
            for design_user in design_users:
                design_notification = Notification(
                    user_id=design_user.id,
                    message=f'New design task #{design_task.id} created for edited CXO article: {article.company_name}',
                    task_id=design_task.id,
                    is_read=False
                )
                db.session.add(design_notification)
        
        db.session.commit()
        
        flash_message = 'Article updated successfully!'
        if was_rejected:
            flash_message += ' Article has been auto-approved and sent to design team.'
        flash(flash_message, 'success')
        return redirect(url_for('cxo.article_detail', article_id=article.id))
    
    brands = Brand.query.all()
    editions = Edition.query.all()
    editors = User.query.filter_by(role='editorial').all()
    
    return render_template('cxo/edit_article.html',
                         user=user,
                         article=article,
                         brands=brands,
                         editions=editions,
                         editors=editors)
