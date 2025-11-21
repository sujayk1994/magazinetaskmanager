import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from app.models import User, Brand, Edition, Task, TaskHistory, TaskFile, CXOArticle, Ad, Notification
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
import random

def seed_comprehensive_data():
    app = create_app()
    with app.app_context():
        print("Clearing existing data...")
        TaskFile.query.delete()
        TaskHistory.query.delete()
        Notification.query.delete()
        Task.query.delete()
        CXOArticle.query.delete()
        Ad.query.delete()
        Edition.query.delete()
        Brand.query.delete()
        User.query.delete()
        db.session.commit()
        
        print("Creating users with managers...")
        default_password = generate_password_hash('password123')
        
        users = [
            User(replit_user_id='super_admin_1', username='super_admin', email='admin@magazine.com', password=default_password, role='super_admin', department='admin', is_manager=True),
            
            User(replit_user_id='cxo_1', username='ceo_john', email='ceo@magazine.com', password=default_password, role='cxo', department='executive', is_manager=True),
            User(replit_user_id='cxo_2', username='cmo_sarah', email='cmo@magazine.com', password=default_password, role='cxo', department='executive', is_manager=False),
            
            User(replit_user_id='sales_manager', username='sales_manager', email='sales_mgr@magazine.com', password=default_password, role='sales', department='sales', is_manager=True),
            User(replit_user_id='sales_1', username='john_sales', email='john@magazine.com', password=default_password, role='sales', department='sales', is_manager=False),
            User(replit_user_id='sales_2', username='mary_sales', email='mary@magazine.com', password=default_password, role='sales', department='sales', is_manager=False),
            
            User(replit_user_id='editorial_manager', username='editorial_manager', email='editorial_mgr@magazine.com', password=default_password, role='editorial', department='editorial', is_manager=True),
            User(replit_user_id='editorial_1', username='editor_jane', email='jane@magazine.com', password=default_password, role='editorial', department='editorial', is_manager=False),
            User(replit_user_id='editorial_2', username='editor_mike', email='mike@magazine.com', password=default_password, role='editorial', department='editorial', is_manager=False),
            User(replit_user_id='editorial_3', username='editor_lisa', email='lisa@magazine.com', password=default_password, role='editorial', department='editorial', is_manager=False),
            
            User(replit_user_id='design_manager', username='design_manager', email='design_mgr@magazine.com', password=default_password, role='design', department='design', is_manager=True),
            User(replit_user_id='design_1', username='designer_sarah', email='sarah@magazine.com', password=default_password, role='design', department='design', is_manager=False),
            User(replit_user_id='design_2', username='designer_david', email='david@magazine.com', password=default_password, role='design', department='design', is_manager=False),
            User(replit_user_id='design_3', username='designer_amy', email='amy@magazine.com', password=default_password, role='design', department='design', is_manager=False),
        ]
        
        for user in users:
            db.session.add(user)
        
        db.session.commit()
        print(f"Created {len(users)} users")
        
        sales_manager = User.query.filter_by(username='sales_manager').first()
        editorial_manager = User.query.filter_by(username='editorial_manager').first()
        design_manager = User.query.filter_by(username='design_manager').first()
        
        john_sales = User.query.filter_by(username='john_sales').first()
        editor_jane = User.query.filter_by(username='editor_jane').first()
        editor_mike = User.query.filter_by(username='editor_mike').first()
        designer_sarah = User.query.filter_by(username='designer_sarah').first()
        designer_david = User.query.filter_by(username='designer_david').first()
        
        print("Creating brands...")
        brands = [
            Brand(name='Tech Magazine', description='Monthly technology magazine'),
            Brand(name='Business Weekly', description='Weekly business publication'),
            Brand(name='Lifestyle Monthly', description='Monthly lifestyle magazine'),
            Brand(name='Finance Today', description='Daily finance news'),
            Brand(name='Innovation Quarterly', description='Quarterly innovation magazine'),
        ]
        
        for brand in brands:
            db.session.add(brand)
        
        db.session.commit()
        print(f"Created {len(brands)} brands")
        
        print("Creating editions...")
        editions = []
        for brand in brands:
            for month in range(1, 7):
                edition = Edition(
                    brand_id=brand.id,
                    name=f"{brand.name} - {datetime(2025, month, 1).strftime('%B %Y')}",
                    year=2025,
                    month=month,
                    status=random.choice(['Scheduled', 'Ongoing', 'Completed'])
                )
                editions.append(edition)
                db.session.add(edition)
        
        db.session.commit()
        print(f"Created {len(editions)} editions")
        
        print("Creating tasks with department assignment workflow...")
        
        task_scenarios = [
            {
                'title': 'Task assigned to Editorial Department',
                'description': 'Sales creates task, assigned to Editorial department, goes to Editorial Manager',
                'created_by': john_sales,
                'assigned_department': 'editorial',
                'assigned_to': editorial_manager,
                'status': 'Assigned',
                'current_department': 'editorial',
                'company_name': 'Tech Corp Inc',
                'category': 'Profile',
                'priority': 'high',
                'history_action': 'Task Created and Assigned to Editorial Department'
            },
            {
                'title': 'Editorial Manager assigns to team member',
                'description': 'Editorial manager received task, then assigned to editor_jane',
                'created_by': john_sales,
                'assigned_department': 'editorial',
                'assigned_to': editor_jane,
                'status': 'InProgress',
                'current_department': 'editorial',
                'company_name': 'Business Solutions Ltd',
                'category': 'Article',
                'priority': 'normal',
                'history_action': 'Assigned to Editorial team member by manager'
            },
            {
                'title': 'Task in Open state for Editorial pickup',
                'description': 'Task assigned to Editorial department, in open state, any editorial team member can pick up',
                'created_by': john_sales,
                'assigned_department': 'editorial',
                'assigned_to': None,
                'status': 'Open',
                'current_department': 'editorial',
                'company_name': 'Marketing Pro Agency',
                'category': 'Profile',
                'priority': 'normal',
                'history_action': 'Task available for Editorial team pickup'
            },
            {
                'title': 'Task sent to Design department',
                'description': 'Editorial completes work, sends to design department, goes to Design Manager',
                'created_by': john_sales,
                'original_requester_id': editor_jane.id,
                'assigned_department': 'design',
                'assigned_to': design_manager,
                'status': 'Assigned',
                'current_department': 'design',
                'company_name': 'Creative Studios',
                'category': 'Cover',
                'priority': 'high',
                'history_action': 'Sent to Design department from Editorial'
            },
            {
                'title': 'Design team member working on task',
                'description': 'Design manager assigned to designer_sarah, now in progress',
                'created_by': john_sales,
                'original_requester_id': editor_mike.id,
                'assigned_department': 'design',
                'assigned_to': designer_sarah,
                'status': 'InProgress',
                'current_department': 'design',
                'company_name': 'Design Hub Co',
                'category': 'AD',
                'priority': 'high',
                'history_action': 'Design team member working on task'
            },
            {
                'title': 'Design completed - returning to Editorial',
                'description': 'Design team completed work, will return to original editorial requester',
                'created_by': john_sales,
                'original_requester_id': editor_jane.id,
                'assigned_department': 'editorial',
                'assigned_to': editor_jane,
                'status': 'Review',
                'current_department': 'editorial',
                'company_name': 'Final Review Co',
                'category': 'Cover',
                'priority': 'high',
                'history_action': 'Design completed, returned to Editorial requester'
            },
            {
                'title': 'Design open task for pickup',
                'description': 'Task in Design department, open for any design team member to pickup',
                'created_by': john_sales,
                'original_requester_id': editor_mike.id,
                'assigned_department': 'design',
                'assigned_to': None,
                'status': 'Open',
                'current_department': 'design',
                'company_name': 'Visual Arts Ltd',
                'category': 'COY Cover',
                'priority': 'normal',
                'history_action': 'Available for Design team pickup'
            },
            {
                'title': 'Multiple department handoffs',
                'description': 'Task that went from Editorial to Design and back',
                'created_by': john_sales,
                'original_requester_id': None,
                'assigned_department': 'editorial',
                'assigned_to': editorial_manager,
                'status': 'Assigned',
                'current_department': 'editorial',
                'company_name': 'Multi Department Inc',
                'category': 'Profile',
                'priority': 'low',
                'history_action': 'New task for editorial'
            },
        ]
        
        tasks = []
        for idx, scenario in enumerate(task_scenarios):
            deadline = datetime.utcnow() + timedelta(days=random.randint(3, 30))
            edition = random.choice(editions)
            
            task = Task(
                brand_id=edition.brand_id,
                edition_id=edition.id,
                created_by_id=scenario['created_by'].id,
                assigned_to_id=scenario['assigned_to'].id if scenario['assigned_to'] else None,
                assigned_department=scenario['assigned_department'],
                original_requester_id=scenario.get('original_requester_id'),
                title=scenario['title'],
                company_name=scenario['company_name'],
                description=scenario['description'],
                category=scenario['category'],
                priority=scenario['priority'],
                status=scenario['status'],
                current_department=scenario['current_department'],
                deadline=deadline,
                created_at=datetime.utcnow() - timedelta(days=idx)
            )
            
            db.session.add(task)
            db.session.flush()
            
            history = TaskHistory(
                task_id=task.id,
                user_id=scenario['created_by'].id,
                action=scenario['history_action'],
                old_value=None,
                new_value=scenario['status'],
                to_department=scenario['current_department'],
                comment=f"Scenario {idx + 1}: {scenario['description']}"
            )
            db.session.add(history)
            
            if scenario['assigned_to']:
                notification = Notification(
                    user_id=scenario['assigned_to'].id,
                    task_id=task.id,
                    message=f"Task #{task.id} assigned to you: {task.title}",
                    is_read=random.choice([True, False])
                )
                db.session.add(notification)
            
            tasks.append(task)
        
        db.session.commit()
        print(f"Created {len(tasks)} tasks demonstrating department workflow")
        
        print("Creating additional tasks for todo list pagination testing...")
        for i in range(20):
            deadline = datetime.utcnow() + timedelta(days=random.randint(5, 45))
            edition = random.choice(editions)
            assignee = random.choice([editorial_manager, editor_jane, editor_mike, designer_sarah, designer_david])
            
            task = Task(
                brand_id=edition.brand_id,
                edition_id=edition.id,
                created_by_id=john_sales.id,
                assigned_to_id=assignee.id,
                assigned_department=assignee.department,
                title=f'Test Task {i+1} for Pagination',
                company_name=f'Company {i+1}',
                description=f'This is test task {i+1} for testing todo list pagination',
                category=random.choice(['Profile', 'Article', 'Cover', 'AD']),
                priority=random.choice(['low', 'normal', 'high']),
                status=random.choice(['Assigned', 'InProgress', 'Review']),
                current_department=assignee.department,
                deadline=deadline,
                created_at=datetime.utcnow() - timedelta(hours=i)
            )
            
            db.session.add(task)
            db.session.flush()
            
            history = TaskHistory(
                task_id=task.id,
                user_id=john_sales.id,
                action='Task Created',
                old_value=None,
                new_value=task.status,
                to_department=assignee.department
            )
            db.session.add(history)
            
            notification = Notification(
                user_id=assignee.id,
                task_id=task.id,
                message=f"Task #{task.id} assigned to you",
                is_read=random.choice([True, False])
            )
            db.session.add(notification)
        
        db.session.commit()
        print("Created 20 additional tasks for pagination testing")
        
        print("Creating CXO Articles...")
        cxo_user = User.query.filter_by(role='cxo').first()
        for i in range(10):
            edition = random.choice(editions)
            article = CXOArticle(
                brand_id=edition.brand_id,
                edition_id=edition.id,
                uploaded_by_id=cxo_user.id,
                company_name=f'CXO Company {i+1}',
                contact_person_name=f'Contact Person {i+1}',
                contact_person_designation='CEO',
                comments=f'Article {i+1} comments',
                status=random.choice(['Pending', 'Approved', 'Rejected']),
                is_used=random.choice([True, False]),
                uploaded_at=datetime.utcnow() - timedelta(days=i)
            )
            db.session.add(article)
        
        db.session.commit()
        print("Created 10 CXO articles")
        
        print("\n" + "="*80)
        print("COMPREHENSIVE SEED DATA CREATED SUCCESSFULLY!")
        print("="*80)
        print("\nUSERS:")
        print("-" * 80)
        for user in User.query.all():
            manager_status = " [MANAGER]" if user.is_manager else ""
            print(f"  {user.username:25} | Role: {user.role:12} | Dept: {user.department:12}{manager_status}")
        
        print("\nDEPARTMENT WORKFLOW DEMONSTRATION:")
        print("-" * 80)
        print("  ✓ Tasks assigned to department go to department manager")
        print("  ✓ Manager can reassign to team members")
        print("  ✓ Open tasks available for any team member to pickup")
        print("  ✓ Design team returns completed work to original editorial requester")
        print("  ✓ Only design manager can override this workflow")
        
        print("\nTASK SCENARIOS CREATED:")
        print("-" * 80)
        for task in tasks[:8]:
            print(f"  #{task.id}: {task.title}")
            print(f"       Status: {task.status} | Dept: {task.current_department} | Assigned: {task.assigned_user.username if task.assigned_user else 'OPEN'}")
        
        print("\nTODO LIST PAGINATION:")
        print("-" * 80)
        print(f"  Total tasks for testing: {Task.query.count()}")
        print(f"  Dashboard shows: 5 recent tasks with 'View All' link")
        print(f"  All Todo List shows: 20 tasks per page with pagination")
        
        print("\n" + "="*80)
        print("READY TO TEST!")
        print("="*80)

if __name__ == '__main__':
    seed_comprehensive_data()
