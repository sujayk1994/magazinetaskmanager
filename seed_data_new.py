from app import create_app, db
from app.models import User, Brand, Edition, Task, TaskHistory, CXOArticle
from datetime import datetime, timedelta

def seed_database():
    app = create_app()
    
    with app.app_context():
        print("Clearing existing data...")
        db.drop_all()
        db.create_all()
        
        print("Creating users...")
        users = [
            User(replit_user_id='super_admin_1', username='super_admin', email='admin@magazine.com', role='super_admin', department='admin'),
            User(replit_user_id='cxo_1', username='ceo_john', email='ceo@magazine.com', role='cxo', department='executive'),
            User(replit_user_id='cxo_2', username='cmo_sarah', email='cmo@magazine.com', role='cxo', department='executive'),
            User(replit_user_id='sales_1', username='sales_manager', email='sales@magazine.com', role='sales', department='sales'),
            User(replit_user_id='sales_2', username='john_sales', email='john@magazine.com', role='sales', department='sales'),
            User(replit_user_id='editorial_1', username='editor_jane', email='jane@magazine.com', role='editorial', department='editorial'),
            User(replit_user_id='editorial_2', username='editor_mike', email='mike@magazine.com', role='editorial', department='editorial'),
            User(replit_user_id='design_1', username='designer_sarah', email='sarah@magazine.com', role='design', department='design'),
            User(replit_user_id='design_2', username='designer_david', email='david@magazine.com', role='design', department='design'),
        ]
        
        for user in users:
            db.session.add(user)
        
        db.session.commit()
        print(f"Created {len(users)} users")
        
        print("Creating brands...")
        brands_data = [
            {'name': 'Tech Monthly', 'description': 'Leading technology magazine'},
            {'name': 'Business Insider', 'description': 'Business and finance publication'},
            {'name': 'Lifestyle Today', 'description': 'Modern lifestyle magazine'},
            {'name': 'Health & Wellness', 'description': 'Health and fitness publication'},
            {'name': 'Auto World', 'description': 'Automotive industry magazine'},
        ]
        
        brands = []
        for brand_data in brands_data:
            brand = Brand(**brand_data)
            db.session.add(brand)
            brands.append(brand)
        
        db.session.commit()
        print(f"Created {len(brands)} brands")
        
        print("Creating editions...")
        editions_data = [
            {'brand_id': 1, 'name': 'January 2025', 'year': 2025, 'month': 1, 'status': 'Ongoing'},
            {'brand_id': 1, 'name': 'February 2025', 'year': 2025, 'month': 2, 'status': 'Scheduled'},
            {'brand_id': 2, 'name': 'Q1 2025', 'year': 2025, 'month': 1, 'status': 'Ongoing'},
            {'brand_id': 2, 'name': 'Q2 2025', 'year': 2025, 'month': 4, 'status': 'Scheduled'},
            {'brand_id': 3, 'name': 'Winter 2025', 'year': 2025, 'month': 1, 'status': 'Completed'},
            {'brand_id': 4, 'name': 'January 2025', 'year': 2025, 'month': 1, 'status': 'Ongoing'},
            {'brand_id': 5, 'name': 'December 2024', 'year': 2024, 'month': 12, 'status': 'Printed'},
        ]
        
        editions = []
        for edition_data in editions_data:
            edition = Edition(**edition_data)
            db.session.add(edition)
            editions.append(edition)
        
        db.session.commit()
        print(f"Created {len(editions)} editions")
        
        print("Creating tasks with categories...")
        categories = ['Profile', 'Article', 'Cover', 'COY Cover', 'COY', 'AD', 'Other']
        task_templates = [
            {
                'brand_id': 1,
                'edition_id': 1,
                'category': 'Profile',
                'title': 'CEO Profile - TechCorp',
                'company_name': 'TechCorp Inc',
                'company_url': 'https://techcorp.com',
                'description': 'Profile feature on TechCorp CEO',
                'status': 'Open',
                'current_department': 'editorial',
                'created_by_id': 4,
                'priority': 'high',
                'deadline': datetime.utcnow() + timedelta(days=7)
            },
            {
                'brand_id': 1,
                'edition_id': 1,
                'category': 'Article',
                'title': 'AI Trends 2025',
                'company_name': 'AI Research Lab',
                'company_url': 'https://ailab.com',
                'description': 'Article on emerging AI trends',
                'status': 'Assigned',
                'current_department': 'editorial',
                'created_by_id': 4,
                'assigned_to_id': 6,
                'priority': 'high',
                'deadline': datetime.utcnow() + timedelta(days=10)
            },
            {
                'brand_id': 1,
                'edition_id': 1,
                'category': 'Cover',
                'title': 'January Cover Design',
                'company_name': None,
                'company_url': None,
                'description': 'Magazine cover design for January issue',
                'status': 'InProgress',
                'current_department': 'design',
                'created_by_id': 4,
                'assigned_to_id': 8,
                'priority': 'high',
                'deadline': datetime.utcnow() + timedelta(days=5)
            },
            {
                'brand_id': 2,
                'edition_id': 3,
                'category': 'COY',
                'title': 'Company of the Year Award',
                'company_name': 'Innovation Corp',
                'company_url': 'https://innovationcorp.com',
                'description': 'COY feature for Q1 2025',
                'status': 'Review',
                'current_department': 'editorial',
                'created_by_id': 5,
                'assigned_to_id': 7,
                'priority': 'high',
                'deadline': datetime.utcnow() + timedelta(days=3)
            },
            {
                'brand_id': 2,
                'edition_id': 3,
                'category': 'AD',
                'title': 'Full Page Ad - Premium Motors',
                'company_name': 'Premium Motors',
                'company_url': 'https://premiummotors.com',
                'description': 'Full page advertisement design',
                'status': 'Open',
                'current_department': 'design',
                'created_by_id': 5,
                'priority': 'normal',
                'deadline': datetime.utcnow() + timedelta(days=15)
            },
            {
                'brand_id': 3,
                'edition_id': 5,
                'category': 'Other',
                'category_other': 'Special Feature',
                'title': 'Lifestyle Special Feature',
                'company_name': 'Wellness Studios',
                'company_url': 'https://wellnessstudios.com',
                'description': 'Special lifestyle feature',
                'status': 'Completed',
                'current_department': 'design',
                'created_by_id': 4,
                'assigned_to_id': 9,
                'completed_at': datetime.utcnow() - timedelta(days=2),
                'priority': 'normal',
                'deadline': datetime.utcnow() - timedelta(days=5)
            },
            {
                'brand_id': 4,
                'edition_id': 6,
                'category': 'Profile',
                'title': 'Fitness Guru Profile',
                'company_name': 'FitLife Academy',
                'company_url': 'https://fitlife.com',
                'description': 'Profile of renowned fitness trainer',
                'status': 'Open',
                'current_department': 'editorial',
                'created_by_id': 5,
                'priority': 'normal',
                'deadline': datetime.utcnow() + timedelta(days=12)
            },
            {
                'brand_id': 1,
                'edition_id': None,
                'edition_other': 'Special Tech Edition 2025',
                'category': 'Article',
                'title': 'Quantum Computing Breakthrough',
                'company_name': 'Quantum Labs',
                'company_url': 'https://quantumlabs.com',
                'description': 'Article on quantum computing advances',
                'status': 'Assigned',
                'current_department': 'editorial',
                'created_by_id': 4,
                'assigned_to_id': 6,
                'priority': 'high',
                'deadline': datetime.utcnow() + timedelta(days=8)
            },
        ]
        
        tasks = []
        for task_data in task_templates:
            task = Task(**task_data)
            db.session.add(task)
            tasks.append(task)
        
        db.session.commit()
        print(f"Created {len(tasks)} tasks")
        
        print("Creating task history entries...")
        for task in tasks:
            history_entry = TaskHistory(
                task_id=task.id,
                user_id=task.created_by_id,
                action='Task Created',
                old_value=None,
                new_value=task.status,
                comment=f"Task created for {task.category or 'general'} category"
            )
            db.session.add(history_entry)
            
            if task.assigned_to_id:
                assign_history = TaskHistory(
                    task_id=task.id,
                    user_id=task.created_by_id,
                    action='Task Assigned',
                    old_value=None,
                    new_value=str(task.assigned_to_id),
                    comment=f"Task assigned to {task.assigned_user.username}"
                )
                db.session.add(assign_history)
        
        db.session.commit()
        print("Created task history entries")
        
        print("Creating CXO articles...")
        cxo_articles_data = [
            {
                'brand_id': 1,
                'edition_id': 1,
                'company_name': 'StartUp Innovations',
                'contact_person_name': 'Mark Johnson',
                'contact_person_designation': 'CEO',
                'company_url': 'https://startupinnovations.com',
                'comments': 'Exclusive article about startup journey',
                'uploaded_by_id': 2,
                'status': 'Pending',
                'is_used': False
            },
            {
                'brand_id': 2,
                'edition_id': 3,
                'company_name': 'Finance Pro',
                'contact_person_name': 'Lisa Chen',
                'contact_person_designation': 'CFO',
                'company_url': 'https://financepro.com',
                'comments': 'Article on financial planning strategies',
                'uploaded_by_id': 3,
                'status': 'Approved',
                'assigned_to_id': 7,
                'is_used': False
            },
            {
                'brand_id': 1,
                'edition_id': None,
                'edition_other': 'Future Tech Edition',
                'company_name': 'VR Solutions',
                'contact_person_name': 'Robert Kim',
                'contact_person_designation': 'CTO',
                'company_url': 'https://vrsolutions.com',
                'comments': 'VR technology advances article',
                'uploaded_by_id': 2,
                'status': 'Pending',
                'is_used': False
            },
        ]
        
        cxo_articles = []
        for article_data in cxo_articles_data:
            article = CXOArticle(**article_data)
            db.session.add(article)
            cxo_articles.append(article)
        
        db.session.commit()
        print(f"Created {len(cxo_articles)} CXO articles")
        
        print("\n" + "="*60)
        print("Database seeding completed successfully!")
        print("="*60)
        print(f"\nSummary:")
        print(f"  Users: {len(users)} (1 Super Admin, 2 CXO, 2 Sales, 2 Editorial, 2 Design)")
        print(f"  Brands: {len(brands)}")
        print(f"  Editions: {len(editions)}")
        print(f"  Tasks: {len(tasks)} (with various categories and statuses)")
        print(f"  CXO Articles: {len(cxo_articles)}")
        print("\nSample Login Usernames:")
        print("  - super_admin (Super Admin)")
        print("  - ceo_john (CXO)")
        print("  - sales_manager (Sales)")
        print("  - editor_jane (Editorial)")
        print("  - designer_sarah (Design)")
        print("="*60)

if __name__ == '__main__':
    seed_database()
