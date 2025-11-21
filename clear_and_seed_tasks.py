from app import create_app, db
from app.models import Task, TaskHistory, TaskFile, User, Brand, Edition, Notification, CXOArticle
from datetime import datetime, timedelta

app = create_app()

def clear_all_tasks():
    """Clear all tasks and related data"""
    with app.app_context():
        print("Clearing all tasks...")
        
        task_ids = [task.id for task in Task.query.all()]
        
        if task_ids:
            Notification.query.filter(Notification.task_id.in_(task_ids)).delete(synchronize_session=False)
            CXOArticle.query.filter(CXOArticle.task_id.in_(task_ids)).delete(synchronize_session=False)
        
        TaskFile.query.delete()
        TaskHistory.query.delete()
        Task.query.delete()
        db.session.commit()
        print("✓ All tasks cleared!")

def seed_sample_tasks():
    """Seed sample tasks for testing the workflow"""
    with app.app_context():
        john_sales = User.query.filter_by(username='john_sales').first()
        editorial_manager = User.query.filter_by(username='editorial_manager').first()
        editor_jane = User.query.filter_by(username='editor_jane').first()
        design_manager = User.query.filter_by(username='design_manager').first()
        designer_sarah = User.query.filter_by(username='designer_sarah').first()
        designer_amy = User.query.filter_by(username='designer_amy').first()
        ceo_john = User.query.filter_by(username='ceo_john').first()
        
        brand = Brand.query.first()
        edition = Edition.query.first()
        
        if not all([john_sales, editorial_manager, editor_jane, design_manager, designer_sarah]):
            print("Error: Required users not found. Please run the main seed script first.")
            return
        
        print("\nSeeding sample tasks for workflow testing...")
        
        tasks = [
            {
                'title': 'Test Task - Ready for Editorial Manager',
                'description': 'New task from Sales, assigned to Editorial Manager',
                'created_by': john_sales,
                'assigned_to': editorial_manager,
                'assigned_department': 'editorial',
                'current_department': 'editorial',
                'status': 'Assigned',
                'company_name': 'Test Company A',
                'category': 'Profile',
                'priority': 'high'
            },
            {
                'title': 'Test Task - Jane Assigned (Editorial Owner)',
                'description': 'Task assigned to Jane by Editorial Manager - Jane is now editorial owner',
                'created_by': john_sales,
                'assigned_to': editor_jane,
                'assigned_department': 'editorial',
                'current_department': 'editorial',
                'editorial_owner_id': editor_jane.id,
                'status': 'Assigned',
                'company_name': 'Test Company B',
                'category': 'Article',
                'priority': 'normal'
            },
            {
                'title': 'Test Task - Sarah Assigned (Design Owner)',
                'description': 'Task in design, assigned to Sarah - Sarah is design owner, Jane is editorial owner',
                'created_by': john_sales,
                'assigned_to': designer_sarah,
                'assigned_department': 'design',
                'current_department': 'design',
                'editorial_owner_id': editor_jane.id,
                'design_owner_id': designer_sarah.id,
                'status': 'Assigned',
                'company_name': 'Test Company C',
                'category': 'Cover',
                'priority': 'high'
            }
        ]
        
        for task_data in tasks:
            task = Task(
                brand_id=brand.id if brand else None,
                edition_id=edition.id if edition else None,
                created_by_id=task_data['created_by'].id,
                assigned_to_id=task_data['assigned_to'].id if task_data.get('assigned_to') else None,
                assigned_department=task_data['assigned_department'],
                current_department=task_data['current_department'],
                editorial_owner_id=task_data.get('editorial_owner_id'),
                design_owner_id=task_data.get('design_owner_id'),
                title=task_data['title'],
                description=task_data['description'],
                company_name=task_data['company_name'],
                category=task_data['category'],
                priority=task_data['priority'],
                status=task_data['status'],
                deadline=datetime.utcnow() + timedelta(days=7)
            )
            db.session.add(task)
        
        db.session.commit()
        print(f"✓ Created {len(tasks)} sample tasks!")
        
        if ceo_john and brand:
            print("\nSeeding CXO article tasks...")
            
            cxo_article = CXOArticle(
                company_name='Test CXO Company',
                contact_person_name='CEO John Doe',
                contact_person_designation='Chief Executive Officer',
                company_url='https://testcompany.com',
                comments='Sample CXO article for testing the workflow',
                uploaded_by_id=ceo_john.id,
                brand_id=brand.id,
                edition_id=edition.id if edition else None,
                status='Pending',
                assigned_to_id=editorial_manager.id if editorial_manager else None
            )
            db.session.add(cxo_article)
            db.session.commit()
            print(f"✓ Created 1 CXO article task!")
        
        print("\nTasks created:")
        print("1. Task for Editorial Manager to assign to Jane")
        print("2. Task with Jane as editorial owner (test: send to Design)")
        print("3. Task with Sarah as design owner (test: send back to Jane)")
        if ceo_john:
            print("4. CXO article pending editorial review")

if __name__ == '__main__':
    import sys
    
    print("=" * 60)
    print("Task Management - Clear & Seed Tasks")
    print("=" * 60)
    
    if len(sys.argv) > 1 and sys.argv[1] == '--clear-only':
        clear_all_tasks()
    else:
        clear_all_tasks()
        seed_sample_tasks()
    
    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)
