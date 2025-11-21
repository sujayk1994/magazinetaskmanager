#!/usr/bin/env python3
"""
Clear Content Script
This script provides options to delete content data while preserving user accounts.

Two modes:
1. Clear Tasks Only - Removes all tasks, notifications, but keeps brands/editions
2. Clear All Content - Removes everything including brands/editions (requires re-seeding or manual brand/edition creation)
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from app.models import (
    User, Brand, Edition, Task, TaskHistory, TaskFile, 
    CXOArticle, Ad, Notification
)

def clear_tasks_only():
    """Clear tasks, notifications, and related data but keep brands/editions"""
    app = create_app()
    with app.app_context():
        print("=" * 80)
        print("CLEARING TASKS AND RELATED DATA (KEEPING BRANDS/EDITIONS)")
        print("=" * 80)
        print("")
        
        # Count current data
        print("Current data counts:")
        print(f"  Tasks: {Task.query.count()}")
        print(f"  Task Files: {TaskFile.query.count()}")
        print(f"  Task History: {TaskHistory.query.count()}")
        print(f"  CXO Articles: {CXOArticle.query.count()}")
        print(f"  Ads: {Ad.query.count()}")
        print(f"  Notifications: {Notification.query.count()}")
        print("")
        print("Will be preserved:")
        print(f"  Users: {User.query.count()}")
        print(f"  Brands: {Brand.query.count()}")
        print(f"  Editions: {Edition.query.count()}")
        print("")
        
        deleted_counts = {}
        
        print("Deleting data...")
        
        print("  Deleting task files...")
        deleted_counts['Task Files'] = TaskFile.query.delete()
        
        print("  Deleting task history...")
        deleted_counts['Task History'] = TaskHistory.query.delete()
        
        print("  Deleting notifications...")
        deleted_counts['Notifications'] = Notification.query.delete()
        
        print("  Deleting tasks...")
        deleted_counts['Tasks'] = Task.query.delete()
        
        print("  Deleting CXO articles...")
        deleted_counts['CXO Articles'] = CXOArticle.query.delete()
        
        print("  Deleting ads...")
        deleted_counts['Ads'] = Ad.query.delete()
        
        # Commit the changes
        db.session.commit()
        
        print("")
        print("=" * 80)
        print("TASKS AND RELATED DATA DELETED SUCCESSFULLY!")
        print("=" * 80)
        print("")
        print("Deleted items:")
        for item, count in deleted_counts.items():
            print(f"  {item}: {count}")
        
        print("")
        print("Preserved data:")
        print(f"  Users: {User.query.count()}")
        print(f"  Brands: {Brand.query.count()}")
        print(f"  Editions: {Edition.query.count()}")
        print("")
        print("✅ Database is clean and ready for new tasks/content.")
        print("✅ Brands and editions are still available for creating new tasks.")
        print("=" * 80)

def clear_all_content():
    """Clear all content data including brands/editions while preserving users"""
    app = create_app()
    with app.app_context():
        print("=" * 80)
        print("CLEARING ALL CONTENT DATA (INCLUDING BRANDS/EDITIONS)")
        print("=" * 80)
        print("")
        
        # Count current data
        print("Current data counts:")
        print(f"  Users: {User.query.count()}")
        print(f"  Brands: {Brand.query.count()}")
        print(f"  Editions: {Edition.query.count()}")
        print(f"  Tasks: {Task.query.count()}")
        print(f"  Task Files: {TaskFile.query.count()}")
        print(f"  Task History: {TaskHistory.query.count()}")
        print(f"  CXO Articles: {CXOArticle.query.count()}")
        print(f"  Ads: {Ad.query.count()}")
        print(f"  Notifications: {Notification.query.count()}")
        print("")
        
        print("⚠️  WARNING: This will delete ALL brands and editions!")
        print("⚠️  After this, you won't be able to create tasks until you:")
        print("    - Re-seed the database: python seed_comprehensive_with_managers.py")
        print("    - OR manually create brands and editions")
        print("")
        
        deleted_counts = {}
        
        print("Deleting all content data...")
        
        print("  Deleting task files...")
        deleted_counts['Task Files'] = TaskFile.query.delete()
        
        print("  Deleting task history...")
        deleted_counts['Task History'] = TaskHistory.query.delete()
        
        print("  Deleting notifications...")
        deleted_counts['Notifications'] = Notification.query.delete()
        
        print("  Deleting tasks...")
        deleted_counts['Tasks'] = Task.query.delete()
        
        print("  Deleting CXO articles...")
        deleted_counts['CXO Articles'] = CXOArticle.query.delete()
        
        print("  Deleting ads...")
        deleted_counts['Ads'] = Ad.query.delete()
        
        print("  Deleting editions...")
        deleted_counts['Editions'] = Edition.query.delete()
        
        print("  Deleting brands...")
        deleted_counts['Brands'] = Brand.query.delete()
        
        # Commit the changes
        db.session.commit()
        
        print("")
        print("=" * 80)
        print("ALL CONTENT DATA DELETED SUCCESSFULLY!")
        print("=" * 80)
        print("")
        print("Deleted items:")
        for item, count in deleted_counts.items():
            print(f"  {item}: {count}")
        
        print("")
        print("Preserved data:")
        print(f"  Users: {User.query.count()} (unchanged)")
        print("")
        print("⚠️  IMPORTANT: Database has no brands/editions now.")
        print("   To create tasks, you need to either:")
        print("   1. Run: python seed_comprehensive_with_managers.py")
        print("   2. Manually create brands and editions through the UI")
        print("=" * 80)

def main():
    """Main function with menu"""
    print("")
    print("=" * 80)
    print("CONTENT CLEANUP UTILITY")
    print("=" * 80)
    print("")
    print("Choose cleanup mode:")
    print("")
    print("1. Clear Tasks Only (Recommended)")
    print("   - Deletes: Tasks, Task Files, Task History, CXO Articles, Ads, Notifications")
    print("   - Keeps: Users, Brands, Editions")
    print("   - Result: Clean slate for tasks, but brands/editions ready for new work")
    print("")
    print("2. Clear All Content")
    print("   - Deletes: Everything except users")
    print("   - Keeps: Only users and authentication data")
    print("   - Result: Completely empty database (requires re-seeding)")
    print("")
    print("3. Cancel")
    print("")
    
    choice = input("Enter your choice (1-3): ").strip()
    
    if choice == '1':
        print("")
        response = input("Confirm: Clear tasks and related data? (yes/no): ")
        if response.lower() == 'yes':
            clear_tasks_only()
        else:
            print("Operation cancelled.")
    elif choice == '2':
        print("")
        response = input("Confirm: Clear ALL content including brands/editions? (yes/no): ")
        if response.lower() == 'yes':
            clear_all_content()
        else:
            print("Operation cancelled.")
    elif choice == '3':
        print("Operation cancelled.")
    else:
        print("Invalid choice. Operation cancelled.")

if __name__ == '__main__':
    main()
