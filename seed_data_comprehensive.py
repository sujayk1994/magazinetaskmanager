from app import create_app, db
from app.models import User, Brand, Edition, Task, TaskFile, TaskHistory, Ad, Notification
from datetime import datetime, timedelta
import random
import os

def seed_database():
    app = create_app()
    
    with app.app_context():
        print("Clearing existing data...")
        db.drop_all()
        
        print("Creating tables...")
        db.create_all()
        
        print("\nCreating users...")
        users_data = [
            {'replit_user_id': 'user_sales_1', 'username': 'sales_manager', 'email': 'sales@magazine.com', 'role': 'sales'},
            {'replit_user_id': 'user_sales_2', 'username': 'john_sales', 'email': 'john@magazine.com', 'role': 'sales'},
            {'replit_user_id': 'user_editorial_1', 'username': 'editor_jane', 'email': 'jane@magazine.com', 'role': 'editorial'},
            {'replit_user_id': 'user_editorial_2', 'username': 'editor_mike', 'email': 'mike@magazine.com', 'role': 'editorial'},
            {'replit_user_id': 'user_design_1', 'username': 'designer_sarah', 'email': 'sarah@magazine.com', 'role': 'design'},
            {'replit_user_id': 'user_design_2', 'username': 'designer_david', 'email': 'david@magazine.com', 'role': 'design'},
            {'replit_user_id': 'user_manager_1', 'username': 'admin', 'email': 'admin@magazine.com', 'role': 'manager'},
        ]
        
        users = {}
        for user_data in users_data:
            user = User(**user_data)
            db.session.add(user)
            users[user_data['role']] = user
            print(f"  Created user: {user.username}")
        
        db.session.commit()
        
        print("\nCreating brands...")
        brands_data = [
            {'name': 'TechToday', 'description': 'Technology and innovation magazine'},
            {'name': 'LifeStyle Monthly', 'description': 'Fashion, travel, and wellness'},
            {'name': 'Business Weekly', 'description': 'Business and finance news'},
            {'name': 'Food & Culture', 'description': 'Culinary arts and cultural exploration'},
            {'name': 'Health Magazine', 'description': 'Health, fitness and wellness'},
        ]
        
        brands = []
        for brand_data in brands_data:
            brand = Brand(**brand_data)
            db.session.add(brand)
            brands.append(brand)
            print(f"  Created brand: {brand.name}")
        
        db.session.commit()
        
        print("\nCreating editions...")
        editions_data = [
            {'brand': brands[0], 'name': 'January 2025', 'year': 2025, 'month': 1, 'status': 'Ongoing'},
            {'brand': brands[0], 'name': 'February 2025', 'year': 2025, 'month': 2, 'status': 'Scheduled'},
            {'brand': brands[0], 'name': 'March 2025', 'year': 2025, 'month': 3, 'status': 'Scheduled'},
            {'brand': brands[1], 'name': 'Winter 2025', 'year': 2025, 'month': 1, 'status': 'Ongoing'},
            {'brand': brands[1], 'name': 'Spring 2025', 'year': 2025, 'month': 3, 'status': 'Scheduled'},
            {'brand': brands[1], 'name': 'Summer 2025', 'year': 2025, 'month': 6, 'status': 'Hold'},
            {'brand': brands[2], 'name': 'Week 3 - January', 'year': 2025, 'month': 1, 'status': 'Ongoing'},
            {'brand': brands[2], 'name': 'Week 4 - January', 'year': 2025, 'month': 1, 'status': 'Completed'},
            {'brand': brands[3], 'name': 'Q1 2025', 'year': 2025, 'month': 1, 'status': 'Ongoing'},
            {'brand': brands[3], 'name': 'Q2 2025', 'year': 2025, 'month': 4, 'status': 'Scheduled'},
            {'brand': brands[4], 'name': 'January-February 2025', 'year': 2025, 'month': 1, 'status': 'Online'},
            {'brand': brands[4], 'name': 'March-April 2025', 'year': 2025, 'month': 3, 'status': 'Scheduled'},
        ]
        
        editions = []
        for edition_data in editions_data:
            brand = edition_data.pop('brand')
            edition = Edition(brand_id=brand.id, **edition_data)
            db.session.add(edition)
            editions.append(edition)
            print(f"  Created edition: {edition.name} for {brand.name}")
        
        db.session.commit()
        
        print("\nCreating tasks...")
        sales_users = [users['sales'], User.query.filter_by(username='john_sales').first()]
        editorial_users = [User.query.filter_by(username='editor_jane').first(), User.query.filter_by(username='editor_mike').first()]
        design_users = [User.query.filter_by(username='designer_sarah').first(), User.query.filter_by(username='designer_david').first()]
        
        companies = [
            'Apple Inc.', 'Google LLC', 'Microsoft Corp', 'Amazon.com', 'Tesla Inc',
            'Meta Platforms', 'Nike Inc', 'Coca-Cola', 'Samsung Electronics', 'Toyota Motors',
            'BMW Group', 'Adidas AG', 'Sony Corporation', 'Dell Technologies', 'Intel Corp'
        ]
        
        websites = [
            'https://apple.com', 'https://google.com', 'https://microsoft.com', 
            'https://amazon.com', 'https://tesla.com', 'https://meta.com',
            'https://nike.com', 'https://coca-cola.com', 'https://samsung.com',
            'https://toyota.com', 'https://bmw.com', 'https://adidas.com',
            'https://sony.com', 'https://dell.com', 'https://intel.com'
        ]
        
        descriptions = [
            'Full page advertisement for new product launch',
            'Double page spread featuring latest collection',
            'Editorial content about company innovation',
            'Interview with CEO about future vision',
            'Product review and comparison article',
            'Sponsored content highlighting sustainability',
            'Feature story on company history',
            'Technology showcase and specifications',
            'Brand partnership announcement',
            'Industry trends and market analysis'
        ]
        
        statuses = ['pending', 'in_progress', 'completed']
        departments = ['editorial', 'design', 'sales']
        priorities = ['low', 'normal', 'high', 'urgent']
        
        tasks = []
        for i in range(30):
            edition = random.choice(editions)
            created_by = random.choice(sales_users)
            
            current_dept = random.choice(departments)
            if current_dept == 'editorial':
                assigned_to = random.choice(editorial_users)
            elif current_dept == 'design':
                assigned_to = random.choice(design_users)
            else:
                assigned_to = random.choice(sales_users)
            
            task = Task(
                edition_id=edition.id,
                created_by_id=created_by.id,
                assigned_to_id=assigned_to.id,
                company_name=companies[i % len(companies)],
                company_website=websites[i % len(websites)],
                description=descriptions[i % len(descriptions)],
                deadline=datetime.now() + timedelta(days=random.randint(5, 60)),
                priority=random.choice(priorities),
                status=random.choice(statuses),
                current_department=current_dept,
                created_at=datetime.now() - timedelta(days=random.randint(1, 30))
            )
            db.session.add(task)
            tasks.append(task)
            print(f"  Created task #{i+1}: {task.company_name} - {task.description[:50]}...")
        
        db.session.commit()
        
        print("\nCreating task history entries...")
        for i, task in enumerate(tasks[:15]):
            history1 = TaskHistory(
                task_id=task.id,
                user_id=task.created_by_id,
                action='Task created',
                from_department='sales',
                to_department='editorial',
                comment=f'New task created for {task.company_name}',
                created_at=task.created_at
            )
            db.session.add(history1)
            
            if task.status in ['in_progress', 'completed']:
                history2 = TaskHistory(
                    task_id=task.id,
                    user_id=task.assigned_to_id,
                    action='Task accepted',
                    from_department=task.current_department,
                    to_department=task.current_department,
                    comment='Working on this task',
                    created_at=task.created_at + timedelta(hours=2)
                )
                db.session.add(history2)
            
            if task.status == 'completed':
                history3 = TaskHistory(
                    task_id=task.id,
                    user_id=task.assigned_to_id,
                    action='Task completed',
                    from_department=task.current_department,
                    to_department='sales',
                    comment='Task finished and ready for review',
                    created_at=task.created_at + timedelta(days=2)
                )
                db.session.add(history3)
        
        db.session.commit()
        print("  Created task history entries")
        
        print("\nCreating task files...")
        os.makedirs('app/static/uploads/tasks', exist_ok=True)
        
        sample_files = [
            'requirements.pdf', 'design_brief.doc', 'reference_image.jpg',
            'final_layout.pdf', 'approved_content.docx', 'logo.png',
            'specifications.txt', 'notes.txt'
        ]
        
        for i, task in enumerate(tasks[:20]):
            for j in range(random.randint(1, 3)):
                original_filename = random.choice(sample_files)
                filename = f"task_{task.id}_{j}_{original_filename}"
                file_path = f"app/static/uploads/tasks/{filename}"
                
                with open(file_path, 'w') as f:
                    f.write(f"Sample file content for task {task.id}")
                
                task_file = TaskFile(
                    task_id=task.id,
                    uploaded_by_id=task.created_by_id if j == 0 else task.assigned_to_id,
                    filename=filename,
                    original_filename=original_filename,
                    file_path=file_path,
                    file_type=original_filename.split('.')[-1],
                    file_size=1024 * random.randint(10, 500),
                    uploaded_at=task.created_at + timedelta(hours=j*6)
                )
                db.session.add(task_file)
        
        db.session.commit()
        print("  Created task files")
        
        print("\nCreating ads...")
        os.makedirs('app/static/uploads/ads', exist_ok=True)
        
        ad_files = ['ad_design_1.jpg', 'ad_design_2.png', 'banner.jpg', 'poster.pdf', 'ad_final.psd']
        
        for i in range(25):
            brand = random.choice(brands)
            edition = random.choice([e for e in editions if e.brand_id == brand.id]) if random.random() > 0.3 else None
            original_filename = random.choice(ad_files)
            filename = f"brand_{brand.id}_{i}_{original_filename}"
            file_path = f"app/static/uploads/ads/{filename}"
            
            with open(file_path, 'w') as f:
                f.write(f"Sample ad content for brand {brand.name}")
            
            ad = Ad(
                brand_id=brand.id,
                edition_id=edition.id if edition else None,
                uploaded_by_id=random.choice(sales_users).id,
                filename=filename,
                original_filename=original_filename,
                file_path=file_path,
                file_type=original_filename.split('.')[-1],
                uploaded_at=datetime.now() - timedelta(days=random.randint(1, 60))
            )
            db.session.add(ad)
        
        db.session.commit()
        print("  Created ads")
        
        print("\nCreating notifications...")
        for user_key in ['editorial', 'design']:
            user_list = editorial_users if user_key == 'editorial' else design_users
            for user in user_list:
                assigned_tasks = Task.query.filter_by(assigned_to_id=user.id).limit(5).all()
                for task in assigned_tasks:
                    notification = Notification(
                        user_id=user.id,
                        task_id=task.id,
                        message=f'New task assigned: {task.company_name} - {task.description[:50]}',
                        is_read=random.choice([True, False]),
                        created_at=task.created_at + timedelta(minutes=5)
                    )
                    db.session.add(notification)
        
        db.session.commit()
        print("  Created notifications")
        
        print("\n" + "="*60)
        print("✓ Database seeded successfully with comprehensive data!")
        print("="*60)
        print("\nTest Users:")
        print("  Sales: sales_manager, john_sales")
        print("  Editorial: editor_jane, editor_mike")
        print("  Design: designer_sarah, designer_david")
        print("  Manager: admin")
        print("\nDatabase Statistics:")
        print(f"  Users: {User.query.count()}")
        print(f"  Brands: {Brand.query.count()}")
        print(f"  Editions: {Edition.query.count()}")
        print(f"  Tasks: {Task.query.count()}")
        print(f"  Task Files: {TaskFile.query.count()}")
        print(f"  Task History: {TaskHistory.query.count()}")
        print(f"  Ads: {Ad.query.count()}")
        print(f"  Notifications: {Notification.query.count()}")
        print("="*60)

if __name__ == '__main__':
    seed_database()
