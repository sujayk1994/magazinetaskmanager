from flask import Blueprint, render_template, request, redirect, url_for, flash, session, send_file
from app import db
from app.models import Ad, Brand, Edition, User
from app.blueprints.auth import login_required, get_current_user
from werkzeug.utils import secure_filename
import os
from datetime import datetime

bp = Blueprint('ads', __name__, url_prefix='/ads')

UPLOAD_FOLDER = 'app/static/uploads/ads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'psd', 'ai', 'eps'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/')
@login_required
def all_ads():
    user = get_current_user()
    brands = Brand.query.all()
    
    search_query = request.args.get('search', '')
    brand_filter = request.args.get('brand', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    
    query = Ad.query
    
    if search_query:
        query = query.filter(Ad.original_filename.ilike(f'%{search_query}%'))
    
    if brand_filter:
        query = query.filter(Ad.brand_id == brand_filter)
    
    if date_from:
        try:
            date_from_obj = datetime.strptime(date_from, '%Y-%m-%d')
            query = query.filter(Ad.uploaded_at >= date_from_obj)
        except:
            pass
    
    if date_to:
        try:
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d')
            query = query.filter(Ad.uploaded_at <= date_to_obj)
        except:
            pass
    
    ads = query.order_by(Ad.uploaded_at.desc()).all()
    
    ads_by_brand = {}
    for ad in ads:
        brand_name = ad.brand.name
        if brand_name not in ads_by_brand:
            ads_by_brand[brand_name] = []
        ads_by_brand[brand_name].append(ad)
    
    return render_template('ads/all_ads.html',
                         user=user,
                         brands=brands,
                         ads_by_brand=ads_by_brand)

@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_ad():
    user = get_current_user()
    
    if request.method == 'POST':
        brand_id = request.form.get('brand_id')
        edition_id = request.form.get('edition_id')
        
        if edition_id == 'none':
            edition_id = None
        
        if 'files' in request.files:
            files = request.files.getlist('files')
            for file in files:
                if file and file.filename and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    unique_filename = f"{brand_id}_{datetime.utcnow().timestamp()}_{filename}"
                    filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
                    
                    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                    file.save(filepath)
                    
                    ad = Ad(
                        brand_id=brand_id,
                        edition_id=edition_id,
                        uploaded_by_id=user.id,
                        filename=unique_filename,
                        original_filename=filename,
                        file_path=filepath,
                        file_type=filename.rsplit('.', 1)[1].lower()
                    )
                    db.session.add(ad)
        
        db.session.commit()
        flash('Ads uploaded successfully!', 'success')
        return redirect(url_for('ads.all_ads'))
    
    brands = Brand.query.all()
    editions = Edition.query.all()
    
    return render_template('ads/upload_ad.html',
                         user=user,
                         brands=brands,
                         editions=editions)

@bp.route('/download/<int:ad_id>')
@login_required
def download_ad(ad_id):
    user = get_current_user()
    ad = Ad.query.get_or_404(ad_id)
    
    is_authorized = False
    
    if user.role == 'manager':
        is_authorized = True
    elif ad.uploaded_by_id == user.id:
        is_authorized = True
    elif ad.edition_id:
        from app.models import Task
        user_tasks_in_edition = Task.query.filter(
            Task.edition_id == ad.edition_id,
            Task.assigned_to_id == user.id
        ).first()
        if user_tasks_in_edition:
            is_authorized = True
    
    if not is_authorized:
        flash('You do not have permission to download this ad.', 'danger')
        return redirect(url_for('ads.all_ads'))
    
    return send_file(ad.file_path, as_attachment=True, download_name=ad.original_filename)

@bp.route('/<int:ad_id>/assign-edition', methods=['POST'])
@login_required
def assign_edition(ad_id):
    ad = Ad.query.get_or_404(ad_id)
    edition_id = request.form.get('edition_id')
    
    if edition_id == 'none':
        ad.edition_id = None
    else:
        ad.edition_id = edition_id
    
    db.session.commit()
    flash('Ad assigned to edition successfully!', 'success')
    return redirect(url_for('ads.all_ads'))
