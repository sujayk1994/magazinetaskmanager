from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import Brand, Edition, Task, CXOArticle
from app.blueprints.auth import login_required, role_required, get_current_user
from datetime import datetime

bp = Blueprint('magazines', __name__, url_prefix='/magazines')

@bp.route('/')
@login_required
def all_magazines():
    user = get_current_user()
    
    search_query = request.args.get('search', '')
    brand_filter = request.args.get('brand', '')
    status_filter = request.args.get('status', '')
    year_filter = request.args.get('year', '')
    
    query = Edition.query
    
    if brand_filter:
        query = query.filter(Edition.brand_id == brand_filter)
    
    if status_filter:
        query = query.filter(Edition.status == status_filter)
    
    if year_filter:
        query = query.filter(Edition.year == int(year_filter))
    
    if search_query:
        query = query.join(Brand).filter(
            (Edition.name.ilike(f'%{search_query}%')) |
            (Brand.name.ilike(f'%{search_query}%'))
        )
    
    editions = query.order_by(Edition.created_at.desc()).all()
    
    magazine_data = []
    for edition in editions:
        task_count = Task.query.filter_by(edition_id=edition.id).count()
        completed_tasks = Task.query.filter_by(edition_id=edition.id, status='completed').count()
        
        magazine_data.append({
            'brand': edition.brand,
            'edition': edition,
            'task_count': task_count,
            'completed_tasks': completed_tasks
        })
    
    brands = Brand.query.all()
    statuses = ['Scheduled', 'Ongoing', 'Hold', 'Canceled', 'Completed', 'Online', 'Printed', 'Shipped']
    years = db.session.query(Edition.year).distinct().filter(Edition.year.isnot(None)).order_by(Edition.year.desc()).all()
    years = [year[0] for year in years]
    
    return render_template('magazines/all_magazines.html',
                         user=user,
                         magazine_data=magazine_data,
                         brands=brands,
                         statuses=statuses,
                         years=years)

@bp.route('/create-brand', methods=['GET', 'POST'])
@login_required
@role_required('sales', 'manager')
def create_brand():
    user = get_current_user()
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        existing_brand = Brand.query.filter_by(name=name).first()
        if existing_brand:
            flash('A brand with this name already exists!', 'danger')
            return redirect(url_for('magazines.create_brand'))
        
        brand = Brand(name=name, description=description)
        db.session.add(brand)
        db.session.commit()
        
        flash('Brand created successfully!', 'success')
        return redirect(url_for('magazines.all_magazines'))
    
    return render_template('magazines/create_brand.html', user=user)

@bp.route('/create-edition', methods=['GET', 'POST'])
@login_required
@role_required('sales', 'manager')
def create_edition():
    user = get_current_user()
    
    if request.method == 'POST':
        brand_id = request.form.get('brand_id')
        name = request.form.get('name')
        year = request.form.get('year')
        month = request.form.get('month')
        
        edition = Edition(
            brand_id=brand_id,
            name=name,
            year=int(year) if year else None,
            month=int(month) if month else None,
            status='Scheduled'
        )
        db.session.add(edition)
        db.session.commit()
        
        flash('Edition created successfully!', 'success')
        return redirect(url_for('magazines.all_magazines'))
    
    brands = Brand.query.all()
    return render_template('magazines/create_edition.html', user=user, brands=brands)

@bp.route('/edition/<int:edition_id>')
@login_required
def edition_detail(edition_id):
    user = get_current_user()
    edition = Edition.query.get_or_404(edition_id)
    tasks = Task.query.filter_by(edition_id=edition_id).all()
    
    return render_template('magazines/edition_detail.html',
                         user=user,
                         edition=edition,
                         tasks=tasks)

@bp.route('/edition/<int:edition_id>/update-status', methods=['POST'])
@login_required
@role_required('design', 'manager')
def update_edition_status(edition_id):
    edition = Edition.query.get_or_404(edition_id)
    new_status = request.form.get('status')
    
    edition.status = new_status
    db.session.commit()
    
    flash('Edition status updated!', 'success')
    return redirect(url_for('magazines.edition_detail', edition_id=edition_id))

@bp.route('/brands')
@login_required
def all_brands():
    user = get_current_user()
    
    if user.role == 'sales' or (user.role in ['design', 'editorial'] and user.is_manager):
        pass
    else:
        flash('You do not have permission to view this page.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    brands = Brand.query.order_by(Brand.name).all()
    
    brand_data = []
    for brand in brands:
        edition_count = Edition.query.filter_by(brand_id=brand.id).count()
        task_count = Task.query.filter_by(brand_id=brand.id).count()
        
        brand_data.append({
            'brand': brand,
            'edition_count': edition_count,
            'task_count': task_count
        })
    
    return render_template('magazines/all_brands.html',
                         user=user,
                         brand_data=brand_data)

@bp.route('/cxo/edition/<int:edition_id>')
@login_required
@role_required('cxo')
def cxo_edition_detail(edition_id):
    user = get_current_user()
    edition = Edition.query.get_or_404(edition_id)
    
    cxo_tasks = Task.query.filter(
        Task.edition_id == edition_id,
        Task.category == 'cxo_article'
    ).all()
    
    return render_template('magazines/cxo_edition_detail.html',
                         user=user,
                         edition=edition,
                         tasks=cxo_tasks)
