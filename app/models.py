from datetime import datetime
from app import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    replit_user_id = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255))
    password = db.Column(db.String(255), nullable=True)
    role = db.Column(db.String(50), nullable=False, default='sales')
    department = db.Column(db.String(50))
    is_manager = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    assigned_tasks = db.relationship('Task', foreign_keys='Task.assigned_to_id', backref='assigned_user', lazy='dynamic')
    created_tasks = db.relationship('Task', foreign_keys='Task.created_by_id', backref='creator', lazy='dynamic')
    notifications = db.relationship('Notification', backref='user', lazy='dynamic', cascade='all, delete-orphan')

class Brand(db.Model):
    __tablename__ = 'brands'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    editions = db.relationship('Edition', backref='brand', lazy='dynamic', cascade='all, delete-orphan')
    ads = db.relationship('Ad', backref='brand', lazy='dynamic', cascade='all, delete-orphan')

class Edition(db.Model):
    __tablename__ = 'editions'
    
    id = db.Column(db.Integer, primary_key=True)
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    status = db.Column(db.String(50), default='Scheduled')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    tasks = db.relationship('Task', backref='edition', lazy='dynamic', cascade='all, delete-orphan')

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'), nullable=True)
    edition_id = db.Column(db.Integer, db.ForeignKey('editions.id'), nullable=True)
    edition_other = db.Column(db.String(200))
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    assigned_department = db.Column(db.String(50))
    original_requester_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    editorial_owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    design_owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    title = db.Column(db.String(200))
    category = db.Column(db.String(50))
    category_other = db.Column(db.String(200))
    company_name = db.Column(db.String(200))
    company_url = db.Column(db.String(255))
    description = db.Column(db.Text)
    deadline = db.Column(db.DateTime)
    priority = db.Column(db.String(20), default='normal')
    
    status = db.Column(db.String(50), default='Open')
    current_department = db.Column(db.String(50), default='editorial')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    archived_at = db.Column(db.DateTime)
    is_archived = db.Column(db.Boolean, default=False)
    
    brand = db.relationship('Brand', backref='tasks')
    original_requester = db.relationship('User', foreign_keys=[original_requester_id], backref='requested_tasks')
    editorial_owner = db.relationship('User', foreign_keys=[editorial_owner_id], backref='owned_editorial_tasks')
    design_owner = db.relationship('User', foreign_keys=[design_owner_id], backref='owned_design_tasks')
    files = db.relationship('TaskFile', backref='task', lazy='dynamic', cascade='all, delete-orphan')
    history = db.relationship('TaskHistory', backref='task', lazy='dynamic', cascade='all, delete-orphan', order_by='TaskHistory.created_at.desc()')

class TaskFile(db.Model):
    __tablename__ = 'task_files'
    
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    uploaded_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    history_id = db.Column(db.Integer, db.ForeignKey('task_history.id'), nullable=True)
    
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_type = db.Column(db.String(50))
    file_size = db.Column(db.Integer)
    version = db.Column(db.Integer, default=1)
    
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)
    is_deleted = db.Column(db.Boolean, default=False)
    
    uploaded_by = db.relationship('User', backref='uploaded_files')

class TaskHistory(db.Model):
    __tablename__ = 'task_history'
    
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    action = db.Column(db.String(100), nullable=False)
    old_value = db.Column(db.Text)
    new_value = db.Column(db.Text)
    from_department = db.Column(db.String(50))
    to_department = db.Column(db.String(50))
    comment = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='task_actions')
    files = db.relationship('TaskFile', backref='history_entry', lazy='dynamic', foreign_keys='TaskFile.history_id')

class Ad(db.Model):
    __tablename__ = 'ads'
    
    id = db.Column(db.Integer, primary_key=True)
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'), nullable=False)
    edition_id = db.Column(db.Integer, db.ForeignKey('editions.id'), nullable=True)
    uploaded_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_type = db.Column(db.String(50))
    
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    uploaded_by = db.relationship('User', backref='uploaded_ads')
    edition = db.relationship('Edition', backref='ads')

class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=True)
    
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    task = db.relationship('Task', backref='notifications')

class CXOArticle(db.Model):
    __tablename__ = 'cxo_articles'
    
    id = db.Column(db.Integer, primary_key=True)
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'), nullable=False)
    edition_id = db.Column(db.Integer, db.ForeignKey('editions.id'), nullable=True)
    edition_other = db.Column(db.String(200))
    uploaded_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=True)
    
    company_name = db.Column(db.String(200))
    contact_person_name = db.Column(db.String(200))
    contact_person_designation = db.Column(db.String(200))
    company_url = db.Column(db.String(255))
    comments = db.Column(db.Text)
    
    status = db.Column(db.String(50), default='Pending')
    is_used = db.Column(db.Boolean, default=False)
    is_archived = db.Column(db.Boolean, default=False)
    
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    used_at = db.Column(db.DateTime)
    archived_at = db.Column(db.DateTime)
    
    brand = db.relationship('Brand', backref='cxo_articles')
    edition = db.relationship('Edition', backref='cxo_articles')
    uploaded_by = db.relationship('User', foreign_keys=[uploaded_by_id], backref='uploaded_articles')
    assigned_to = db.relationship('User', foreign_keys=[assigned_to_id], backref='assigned_articles')
    task = db.relationship('Task', backref='cxo_article', foreign_keys=[task_id])
    files = db.relationship('CXOArticleFile', backref='article', lazy=True, cascade='all, delete-orphan')
    
    def sync_with_task(self):
        if not self.task:
            return
        
        self.assigned_to_id = self.task.assigned_to_id
        
        if self.is_used:
            self.status = 'Used'
        elif self.status == 'Rejected':
            pass
        elif self.task.current_department == 'design':
            if self.task.status == 'Completed':
                self.status = 'Design Ready'
            elif self.task.assigned_to_id is not None:
                self.status = 'Designing'
            else:
                self.status = 'Awaiting Design'
        elif self.task.current_department == 'editorial':
            if self.task.status == 'Completed':
                self.status = 'Approved'
            else:
                self.status = 'Pending'
        
        self.updated_at = datetime.utcnow()

class CXOArticleFile(db.Model):
    __tablename__ = 'cxo_article_files'
    
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('cxo_articles.id'), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    stored_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_type = db.Column(db.String(50))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
