# Magazine Task Management System - Technical Documentation

## Table of Contents
1. [System Architecture](#system-architecture)
2. [Database Schema](#database-schema)
3. [Routing Logic](#routing-logic)
4. [Task Ownership System](#task-ownership-system)
5. [Role-Based Access Control](#role-based-access-control)
6. [API Endpoints](#api-endpoints)
7. [File Upload System](#file-upload-system)
8. [Notification System](#notification-system)
9. [Code Structure](#code-structure)
10. [Key Algorithms](#key-algorithms)

---

## System Architecture

### Technology Stack

**Backend**:
- Python 3.11
- Flask 3.0.0 (Web Framework)
- SQLAlchemy (ORM)
- PostgreSQL 15 (Database)
- Flask-Migrate (Database Migrations)

**Frontend**:
- Jinja2 Templates
- Bootstrap 5 (CSS Framework)
- JavaScript (Vanilla)
- Bootstrap Icons

**Deployment**:
- Gunicorn (WSGI Server)
- Replit (Primary Platform)
- Docker (Alternative Deployment)

### Application Structure

```
magazine-task-management/
├── app/
│   ├── __init__.py              # App factory
│   ├── models.py                # Database models
│   ├── blueprints/              # Route blueprints
│   │   ├── auth.py              # Authentication
│   │   ├── main.py              # Main routes
│   │   ├── tasks.py             # Task management
│   │   ├── magazines.py         # Brand/Edition management
│   │   ├── ads.py               # Ads management
│   │   └── cxo.py               # CXO articles
│   ├── templates/               # HTML templates
│   │   ├── base.html            # Base template
│   │   ├── auth/                # Auth templates
│   │   ├── tasks/               # Task templates
│   │   ├── magazines/           # Magazine templates
│   │   ├── ads/                 # Ads templates
│   │   └── cxo/                 # CXO templates
│   └── static/                  # Static files
│       ├── css/                 # Stylesheets
│       ├── js/                  # JavaScript
│       └── uploads/             # File uploads
├── migrations/                  # Database migrations
├── config.py                    # Configuration
├── main.py                      # Application entry point
├── seed_comprehensive_with_managers.py  # Data seeding
└── requirements.txt             # Python dependencies
```

---

## Database Schema

### Entity Relationship Diagram

```
User (14 test users)
  ├── has many → Task (as creator)
  ├── has many → Task (as assigned_user)
  ├── has many → Task (as editorial_owner)
  ├── has many → Task (as design_owner)
  ├── has many → Task (as original_requester)
  ├── has many → TaskHistory
  ├── has many → TaskFile (as uploader)
  └── has many → Notification

Brand (5 brands)
  ├── has many → Edition
  ├── has many → Task
  └── has many → Ad

Edition (30 editions)
  └── has many → Task

Task (28 tasks)
  ├── belongs to → User (creator)
  ├── belongs to → User (assigned_user)
  ├── belongs to → User (editorial_owner)
  ├── belongs to → User (design_owner)
  ├── belongs to → User (original_requester)
  ├── belongs to → Brand
  ├── belongs to → Edition
  ├── has many → TaskFile
  ├── has many → TaskHistory
  └── has one → CXOArticle

TaskFile (file uploads)
  ├── belongs to → Task
  ├── belongs to → User (uploader)
  └── belongs to → TaskHistory (optional)

TaskHistory (audit trail)
  ├── belongs to → Task
  ├── belongs to → User
  └── has many → TaskFile

Notification
  ├── belongs to → User
  └── belongs to → Task

CXOArticle
  └── belongs to → Task (optional)

Ad
  └── belongs to → Brand
```

### Database Tables

#### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    replit_user_id VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(255),
    password VARCHAR(255) DEFAULT 'password123',
    role VARCHAR(50) NOT NULL DEFAULT 'sales',
    department VARCHAR(50),
    is_manager BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Indexes**:
- Primary Key: `id`
- Unique: `replit_user_id`, `username`
- Index: `role`, `department`, `is_manager`

**Roles**: super_admin, cxo, sales, editorial, design
**Departments**: admin, executive, sales, editorial, design

---

#### Tasks Table
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    brand_id INTEGER REFERENCES brands(id),
    edition_id INTEGER REFERENCES editions(id),
    edition_other VARCHAR(200),
    created_by_id INTEGER REFERENCES users(id) NOT NULL,
    assigned_to_id INTEGER REFERENCES users(id),
    assigned_department VARCHAR(50),
    original_requester_id INTEGER REFERENCES users(id),
    editorial_owner_id INTEGER REFERENCES users(id),
    design_owner_id INTEGER REFERENCES users(id),
    title VARCHAR(200),
    category VARCHAR(50),
    category_other VARCHAR(200),
    company_name VARCHAR(200),
    company_url VARCHAR(255),
    description TEXT,
    deadline TIMESTAMP,
    priority VARCHAR(20) DEFAULT 'normal',
    status VARCHAR(50) DEFAULT 'Open',
    current_department VARCHAR(50) DEFAULT 'editorial',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    archived_at TIMESTAMP,
    is_archived BOOLEAN DEFAULT FALSE
);
```

**Key Fields**:
- `original_requester_id`: Editorial person who first sent to design
- `editorial_owner_id`: Editorial person in the loop
- `design_owner_id`: Design person in the loop
- `assigned_to_id`: Current task assignee
- `current_department`: Current department handling task

**Statuses**: Open, Assigned, InProgress, Review, Completed, Archived

**Priorities**: low, normal, high

**Categories**: Profile, Article, Cover, AD, Profile Picture, COY Cover, Column, Other

---

#### Task History Table
```sql
CREATE TABLE task_history (
    id SERIAL PRIMARY KEY,
    task_id INTEGER REFERENCES tasks(id) NOT NULL,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    action VARCHAR(100) NOT NULL,
    old_value TEXT,
    new_value TEXT,
    from_department VARCHAR(50),
    to_department VARCHAR(50),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Actions**:
- Task Created
- Task Assigned by Manager
- Task Picked Up
- Editorial Completed - Sent to Design
- Design Completed - Sent to Editorial
- Sent to Sales for Client Feedback
- Sent Back to Manager
- Task Completed
- Task Archived

---

## Routing Logic

### Task Routing State Machine

```
┌─────────────┐
│ Sales       │
│ Creates Task│
└──────┬──────┘
       │
       v
┌─────────────────┐
│ Editorial Mgr   │ (First Time)
│ (General Pool)  │
└──────┬──────────┘
       │
       │ Manager Assigns
       v
┌──────────────────┐
│ Editorial Owner  │ (Jane)
│ [editorial_owner │
│  _id set]        │
└──────┬───────────┘
       │
       │ Send to Design
       v
┌──────────────────┐
│ Design Manager   │ (First Time)
│ (General Pool)   │
└──────┬───────────┘
       │
       │ Manager Assigns
       v
┌──────────────────┐
│ Design Owner     │ (Sarah)
│ [design_owner_id │
│  set]            │
└──────┬───────────┘
       │
       └──────────┐
                  │
         ┌────────┴────────┐
         │                 │
         │  THE LOOP       │
         │  BEGINS         │
         │                 │
    ┌────v────┐       ┌────v────┐
    │ Sarah   │◄──────┤ Jane    │
    │ (Design)│       │(Editorial)│
    └────┬────┘       └────┬────┘
         │                 │
         └────────►────────┘
              Loop
          Forever Until:
          - Manager Override
          - Send to Sales
          - Task Archived
```

### Routing Rules

#### Rule 1: First-Time Assignment
```python
if not task.editorial_owner_id:
    # Goes to Editorial Manager
    next_user = editorial_manager
else:
    # Goes to Editorial Owner
    next_user = task.editorial_owner
```

#### Rule 2: Design Assignment
```python
if not task.design_owner_id:
    # First time → Design Manager
    next_user = design_manager
else:
    # Subsequent sends → Design Owner
    next_user = task.design_owner
```

#### Rule 3: Manager Override
```python
# Manager can always reassign
task.design_owner_id = new_designer.id
# This updates the loop
# New loop: new_designer ↔ editorial_owner
```

#### Rule 4: Design Completion
```python
if not user.is_manager:
    # Regular designer → returns to editorial
    task.assigned_to_id = task.original_requester_id
else:
    # Manager can complete without returning
    task.status = 'Completed'
```

---

## Task Ownership System

### Ownership Fields Explained

#### 1. `created_by_id`
- **Set**: When task is created
- **Purpose**: Track who created the task
- **Never Changes**: Permanent record
- **Usage**: For reporting, audit trail

#### 2. `assigned_to_id`
- **Set**: Current assignee
- **Purpose**: Who is working on task now
- **Changes**: Frequently (every handoff)
- **Usage**: "My Tasks" filtering, notifications

#### 3. `original_requester_id`
- **Set**: When editorial first sends to design
- **Purpose**: Remember who requested design work
- **Usage**: Return path from design to editorial

#### 4. `editorial_owner_id`
- **Set**: When manager assigns to editorial team member
- **Purpose**: Create editorial anchor in loop
- **Usage**: Return path from design, loop establishment

#### 5. `design_owner_id`
- **Set**: When manager assigns to design team member
- **Purpose**: Create design anchor in loop
- **Usage**: Direct sends from editorial, loop establishment

### Ownership Lifecycle

```
Task Created
├── created_by_id = john_sales
├── assigned_to_id = editorial_manager
└── All ownership fields = NULL

Editorial Manager Assigns to Jane
├── assigned_to_id = editor_jane
└── editorial_owner_id = editor_jane  ✓ SET

Jane Sends to Design
├── assigned_to_id = design_manager
├── original_requester_id = editor_jane  ✓ SET
└── design_owner_id = NULL (not yet)

Design Manager Assigns to Sarah
├── assigned_to_id = designer_sarah
└── design_owner_id = designer_sarah  ✓ SET

Sarah Sends Back (Loop Begins)
├── assigned_to_id = editor_jane  (uses editorial_owner_id)
└── Loop: Sarah ↔ Jane established

Jane Sends to Design Again
├── assigned_to_id = designer_sarah  (uses design_owner_id)
└── Loop continues

Design Manager Reassigns to Amy (Override)
├── assigned_to_id = designer_amy
└── design_owner_id = designer_amy  ✓ CHANGED

New Loop
└── Loop: Amy ↔ Jane established
```

---

## Role-Based Access Control

### Permission Matrix

| Action | Super Admin | CXO | Sales Mgr | Sales | Editorial Mgr | Editorial | Design Mgr | Design |
|--------|-------------|-----|-----------|-------|---------------|-----------|------------|--------|
| View All Tasks | ✓ | ✓ | Dept Only | Assigned | Dept Only | Assigned | Dept Only | Assigned |
| Create Task | ✓ | ✗ | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| Assign to Team | ✓ | ✗ | ✓ | ✗ | ✓ | ✗ | ✓ | ✗ |
| Mark Open | ✓ | ✗ | ✓ | ✗ | ✓ | ✗ | ✓ | ✗ |
| Pick Up Open | ✓ | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Send to Design | ✓ | ✗ | ✗ | ✗ | ✓ | ✓ | ✗ | ✗ |
| Send to Editorial | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ |
| Send to Sales | ✓ | ✗ | ✗ | ✗ | ✓ | ✓ | ✗ | ✗ |
| Complete Task | ✓ | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Archive Task | ✓ | ✗ | ✓ | ✗ | ✓ | ✗ | ✓ | ✗ |
| Create Brand | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Create Edition | ✓ | ✗ | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| Upload CXO Article | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Upload Ad | ✓ | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ |

### Authentication Decorators

#### `@login_required`
```python
@bp.route('/dashboard')
@login_required
def dashboard():
    # User must be logged in
    pass
```

#### `@role_required('editorial', 'design')`
```python
@bp.route('/send_to_design')
@role_required('editorial')
def send_to_design():
    # Only editorial users can access
    pass
```

#### `@super_admin_required`
```python
@bp.route('/admin/brands')
@super_admin_required
def manage_brands():
    # Only super admin can access
    pass
```

### Manager Checks

```python
def assign_to_member(task_id):
    if not user.is_manager:
        flash('Only managers can assign tasks')
        return redirect('/')
    
    if user.department != task.current_department:
        flash('Can only assign tasks in your department')
        return redirect('/')
    
    # Proceed with assignment
```

---

## API Endpoints

### Authentication Routes (`/auth`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/login` | Display login page | No |
| POST | `/login` | Process login | No |
| GET | `/callback` | Replit OAuth callback | No |
| GET | `/logout` | Logout user | No |

### Main Routes (`/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | Landing page | No |
| GET | `/dashboard` | User dashboard | Yes |
| GET | `/cxo-dashboard` | CXO dashboard | Yes (CXO) |
| GET | `/manager-dashboard` | Manager dashboard | Yes (Manager) |

### Task Routes (`/tasks`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/tasks/create` | Create task form | Yes |
| POST | `/tasks/create` | Submit new task | Yes |
| GET | `/tasks/my-tasks` | My assigned tasks | Yes |
| GET | `/tasks/all-tasks` | All viewable tasks | Yes |
| GET | `/tasks/open-tasks` | Open tasks for pickup | Yes |
| GET | `/tasks/<id>` | Task detail page | Yes |
| POST | `/tasks/<id>/complete` | Mark task complete | Yes |
| POST | `/tasks/<id>/pickup` | Pick up open task | Yes |
| POST | `/tasks/<id>/assign_to_member` | Assign to team member | Yes (Manager) |
| POST | `/tasks/<id>/send_back_to_editor` | Send to editorial | Yes (Design) |
| POST | `/tasks/<id>/send_to_sales` | Send to sales | Yes (Editorial) |
| POST | `/tasks/<id>/send_back_to_manager` | Send to manager | Yes |
| POST | `/tasks/<id>/archive` | Archive task | Yes (Manager) |
| POST | `/tasks/<id>/upload_file` | Upload file to task | Yes |
| POST | `/tasks/<id>/add_comment` | Add comment | Yes |

### Magazine Routes (`/magazines`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/magazines` | List all brands | Yes |
| GET | `/magazines/create-brand` | Create brand form | Yes (Admin) |
| POST | `/magazines/create-brand` | Submit new brand | Yes (Admin) |
| GET | `/magazines/editions` | List all editions | Yes |
| GET | `/magazines/create-edition` | Create edition form | Yes |
| POST | `/magazines/create-edition` | Submit new edition | Yes |
| GET | `/magazines/edition/<id>` | Edition detail | Yes |

### CXO Routes (`/cxo`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/cxo/articles` | List all articles | Yes (CXO) |
| GET | `/cxo/upload` | Upload article form | Yes (CXO) |
| POST | `/cxo/upload` | Submit new article | Yes (CXO) |

### Ads Routes (`/ads`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/ads` | List all ads | Yes |
| GET | `/ads/upload` | Upload ad form | Yes |
| POST | `/ads/upload` | Submit new ad | Yes |

---

## File Upload System

### Configuration

```python
UPLOAD_FOLDER = 'app/static/uploads'
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB
ALLOWED_EXTENSIONS = {
    'pdf', 'png', 'jpg', 'jpeg', 'gif',
    'doc', 'docx', 'txt',
    'mp3', 'wav', 'mp4'
}
```

### Upload Process

1. **Client sends file**
   ```html
   <form method="POST" enctype="multipart/form-data">
       <input type="file" name="files" multiple>
   </form>
   ```

2. **Server validates file**
   ```python
   def allowed_file(filename):
       return '.' in filename and \
              filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
   ```

3. **Generate unique filename**
   ```python
   import uuid
   unique_filename = f"{uuid.uuid4()}_{original_filename}"
   ```

4. **Save to disk**
   ```python
   filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
   file.save(filepath)
   ```

5. **Create database record**
   ```python
   task_file = TaskFile(
       task_id=task.id,
       uploaded_by_id=user.id,
       filename=unique_filename,
       original_filename=original_filename,
       file_path=filepath,
       file_type=file_type,
       file_size=file_size
   )
   db.session.add(task_file)
   ```

### File Versioning

- Each upload creates new record
- Files never deleted (soft delete with `is_deleted`)
- Version tracking in `version` field
- History linked via `history_id`

---

## Notification System

### When Notifications Are Created

```python
# Task assigned to user
Notification(
    user_id=assignee.id,
    task_id=task.id,
    message=f'Task #{task.id} assigned to you'
)

# Task sent to user
Notification(
    user_id=recipient.id,
    task_id=task.id,
    message=f'Task #{task.id} sent to you by {sender.username}'
)

# Task status changed
Notification(
    user_id=owner.id,
    task_id=task.id,
    message=f'Task #{task.id} status changed to {new_status}'
)
```

### Notification Display

```python
# Get unread count
unread_count = Notification.query.filter_by(
    user_id=user.id,
    is_read=False
).count()

# Get recent notifications
notifications = Notification.query.filter_by(
    user_id=user.id
).order_by(Notification.created_at.desc()).limit(10)
```

### Mark as Read

```python
# Mark specific notification
notification.is_read = True
db.session.commit()

# Mark all as read
Notification.query.filter_by(
    user_id=user.id,
    is_read=False
).update({'is_read': True})
```

---

## Code Structure

### Application Factory Pattern

```python
# app/__init__.py
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(tasks.bp)
    
    return app
```

### Blueprint Structure

```python
# app/blueprints/tasks.py
bp = Blueprint('tasks', __name__, url_prefix='/tasks')

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_task():
    pass
```

### Helper Functions

```python
# Get current user from session
def get_current_user():
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None

# Get role-based redirect
def get_role_based_redirect(user_role):
    role_redirects = {
        'cxo': 'main.cxo_dashboard',
        # ...
    }
    return url_for(role_redirects.get(user_role, 'main.dashboard'))
```

---

## Key Algorithms

### Task Assignment Algorithm

```python
def assign_task_to_department(task, department):
    """
    Assigns task to appropriate user based on ownership
    """
    if department == 'editorial':
        if task.editorial_owner_id:
            # Has owner → direct assignment
            next_user = task.editorial_owner
        else:
            # No owner → manager assignment
            next_user = get_department_manager('editorial')
    
    elif department == 'design':
        if task.design_owner_id:
            # Has owner → direct assignment
            next_user = task.design_owner
        else:
            # No owner → manager assignment
            next_user = get_department_manager('design')
    
    task.assigned_to_id = next_user.id
    task.current_department = department
    db.session.commit()
    
    return next_user
```

### Loop Detection Algorithm

```python
def get_task_loop_participants(task):
    """
    Identifies users in the editorial-design loop
    """
    participants = []
    
    if task.editorial_owner_id:
        participants.append({
            'user': task.editorial_owner,
            'department': 'editorial',
            'role': 'owner'
        })
    
    if task.design_owner_id:
        participants.append({
            'user': task.design_owner,
            'department': 'design',
            'role': 'owner'
        })
    
    return participants
```

### Task History Builder

```python
def create_task_history(task, user, action, **kwargs):
    """
    Creates audit trail entry
    """
    history = TaskHistory(
        task_id=task.id,
        user_id=user.id,
        action=action,
        old_value=kwargs.get('old_value'),
        new_value=kwargs.get('new_value'),
        from_department=kwargs.get('from_dept'),
        to_department=kwargs.get('to_dept'),
        comment=kwargs.get('comment')
    )
    db.session.add(history)
    return history
```

---

## Performance Considerations

### Database Queries

**Eager Loading**:
```python
# Load task with relationships
task = Task.query.options(
    db.joinedload(Task.assigned_user),
    db.joinedload(Task.creator),
    db.joinedload(Task.brand),
    db.joinedload(Task.edition)
).get(task_id)
```

**Indexed Queries**:
```python
# Fast lookup by status and department
tasks = Task.query.filter_by(
    status='Assigned',
    current_department='editorial'
).all()
```

### Caching Strategy

- Static files cached via nginx
- Session data in cookies
- Query results not cached (real-time data)

### File Upload Optimization

- Client-side file size validation
- Chunked upload for large files (future)
- Background processing for media (future)

---

## Security Considerations

### Password Hashing

```python
from werkzeug.security import generate_password_hash, check_password_hash

# Hash password
hashed = generate_password_hash('password123')

# Verify password
check_password_hash(hashed, 'password123')  # True
```

### SQL Injection Prevention

- SQLAlchemy ORM (parameterized queries)
- No raw SQL without parameterization

### File Upload Security

- Filename sanitization
- Type validation
- Size limits
- Unique filenames (UUID)
- Storage outside web root

### Session Security

```python
SESSION_SECRET = 'random-secret-key'
session.permanent = True
PERMANENT_SESSION_LIFETIME = timedelta(days=7)
```

---

## Testing

### Manual Testing Checklist

**Authentication**:
- [x] Login with valid credentials
- [x] Login with invalid credentials
- [x] Logout
- [x] Session persistence

**Task Creation**:
- [x] Create task as sales
- [x] All required fields validation
- [x] File upload
- [x] Department assignment

**Task Workflow**:
- [x] Manager assigns to team member
- [x] Team member picks up open task
- [x] Send to design (first time → manager)
- [x] Design manager assigns
- [x] Send back to editorial (owner established)
- [x] Loop: editorial ↔ design
- [x] Manager override (new designer)
- [x] New loop with new designer
- [x] Send to sales
- [x] Task completion

**Permissions**:
- [x] Role-based access control
- [x] Manager-only actions
- [x] Cross-department restrictions

---

## Error Handling

### Common Errors

**404 Not Found**:
```python
task = Task.query.get_or_404(task_id)
```

**403 Forbidden**:
```python
if user.role not in allowed_roles:
    flash('Permission denied', 'danger')
    return redirect('/')
```

**500 Internal Error**:
```python
try:
    db.session.commit()
except Exception as e:
    db.session.rollback()
    flash('An error occurred', 'danger')
    app.logger.error(f'Error: {e}')
```

---

## Logging

### Log Levels

```python
import logging

# Info level
app.logger.info('User logged in: %s', username)

# Warning level
app.logger.warning('Invalid login attempt: %s', username)

# Error level
app.logger.error('Database error: %s', str(e))
```

### Log Format

```
[2025-11-21 14:00:00,000] INFO in auth: User logged in: john_sales
[2025-11-21 14:00:05,123] WARNING in tasks: Task not found: 999
[2025-11-21 14:00:10,456] ERROR in main: Database connection failed
```

---

## Future Enhancements

### Planned Features

1. **Real-time Notifications**
   - WebSocket integration
   - Push notifications
   - Live task updates

2. **Advanced Search**
   - Full-text search
   - Advanced filters
   - Saved searches

3. **Analytics Dashboard**
   - Task completion metrics
   - Department performance
   - Timeline analytics

4. **Email Integration**
   - Email notifications
   - Task updates via email
   - Email-to-task creation

5. **API Access**
   - REST API
   - API authentication
   - Third-party integrations

6. **Mobile App**
   - React Native app
   - Push notifications
   - Offline support

---

## Contributing

### Code Style

- PEP 8 for Python
- 4 spaces indentation
- Meaningful variable names
- Comments for complex logic

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/task-tags

# Make changes and commit
git add .
git commit -m "Add task tagging feature"

# Push to remote
git push origin feature/task-tags

# Create pull request
```

---

## Support & Maintenance

### Backup Strategy

- Daily database backups
- Weekly full backups
- File uploads backed up separately
- Test restore procedures monthly

### Monitoring

- Application logs
- Database performance
- Disk space usage
- Error rates

### Updates

- Security patches: Immediate
- Bug fixes: Weekly
- Features: Monthly
- Major releases: Quarterly

---

**Last Updated**: November 2025
**Version**: 1.0.0
**Maintained By**: Development Team

---

## Glossary

**Task Owner**: User permanently assigned to handle tasks in a department
**Loop**: Repeating workflow between editorial and design owners
**Open Task**: Task available for any team member to pick up
**Manager Override**: Manager reassigns task, changing ownership
**Original Requester**: Editorial user who first sent task to design
**Department**: Organizational unit (sales, editorial, design)
**Role**: User permission level (super_admin, cxo, sales, editorial, design)
**Status**: Task state (Open, Assigned, InProgress, Review, Completed)
**Priority**: Task urgency (low, normal, high)

---

*For questions or clarifications, please contact the development team.*
