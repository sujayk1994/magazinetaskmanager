from app import create_app, db
from app.models import User, Brand, Edition
from datetime import datetime

def seed_database():
    app = create_app()
    
    with app.app_context():
        print("Creating tables...")
        db.create_all()
        
        print("Creating users...")
        users_data = [
            {'replit_user_id': 'user_sales_1', 'username': 'sales_manager', 'email': 'sales@magazine.com', 'role': 'sales'},
            {'replit_user_id': 'user_sales_2', 'username': 'john_sales', 'email': 'john@magazine.com', 'role': 'sales'},
            {'replit_user_id': 'user_editorial_1', 'username': 'editor_jane', 'email': 'jane@magazine.com', 'role': 'editorial'},
            {'replit_user_id': 'user_editorial_2', 'username': 'editor_mike', 'email': 'mike@magazine.com', 'role': 'editorial'},
            {'replit_user_id': 'user_design_1', 'username': 'designer_sarah', 'email': 'sarah@magazine.com', 'role': 'design'},
            {'replit_user_id': 'user_design_2', 'username': 'designer_david', 'email': 'david@magazine.com', 'role': 'design'},
            {'replit_user_id': 'user_manager_1', 'username': 'admin', 'email': 'admin@magazine.com', 'role': 'manager'},
        ]
        
        for user_data in users_data:
            existing = User.query.filter_by(replit_user_id=user_data['replit_user_id']).first()
            if not existing:
                user = User(**user_data)
                db.session.add(user)
                print(f"  Created user: {user.username}")
        
        db.session.commit()
        
        print("\nCreating brands...")
        brands_data = [
            {'name': 'TechToday', 'description': 'Technology and innovation magazine'},
            {'name': 'LifeStyle Monthly', 'description': 'Fashion, travel, and wellness'},
            {'name': 'Business Weekly', 'description': 'Business and finance news'},
        ]
        
        for brand_data in brands_data:
            existing = Brand.query.filter_by(name=brand_data['name']).first()
            if not existing:
                brand = Brand(**brand_data)
                db.session.add(brand)
                print(f"  Created brand: {brand.name}")
        
        db.session.commit()
        
        print("\nCreating editions...")
        tech_brand = Brand.query.filter_by(name='TechToday').first()
        lifestyle_brand = Brand.query.filter_by(name='LifeStyle Monthly').first()
        business_brand = Brand.query.filter_by(name='Business Weekly').first()
        
        editions_data = [
            {'brand_id': tech_brand.id, 'name': 'January 2025', 'year': 2025, 'month': 1, 'status': 'Ongoing'},
            {'brand_id': tech_brand.id, 'name': 'February 2025', 'year': 2025, 'month': 2, 'status': 'Scheduled'},
            {'brand_id': lifestyle_brand.id, 'name': 'Winter 2025', 'year': 2025, 'month': 1, 'status': 'Ongoing'},
            {'brand_id': lifestyle_brand.id, 'name': 'Spring 2025', 'year': 2025, 'month': 3, 'status': 'Scheduled'},
            {'brand_id': business_brand.id, 'name': 'Week 3 - January', 'year': 2025, 'month': 1, 'status': 'Ongoing'},
        ]
        
        for edition_data in editions_data:
            existing = Edition.query.filter_by(
                brand_id=edition_data['brand_id'],
                name=edition_data['name']
            ).first()
            if not existing:
                edition = Edition(**edition_data)
                db.session.add(edition)
                brand_name = Brand.query.get(edition_data['brand_id']).name
                print(f"  Created edition: {edition.name} for {brand_name}")
        
        db.session.commit()
        
        print("\n✓ Database seeded successfully!")
        print("\nTest Users:")
        print("  Sales: sales_manager, john_sales")
        print("  Editorial: editor_jane, editor_mike")
        print("  Design: designer_sarah, designer_david")
        print("  Manager: admin")

if __name__ == '__main__':
    seed_database()
