# Database Setup Instructions

This document provides instructions for setting up the database with the comprehensive seed data that includes all the new features.

## Features Implemented

### 1. User Management
- Added `is_manager` field to User model
- Department managers can receive and manage tasks for their team

### 2. Task Department Assignment
- Added `assigned_department` field to Task model
- Tasks can be assigned to departments (editorial, design, sales)
- Tasks go to department manager by default
- Managers can reassign to team members or let team pickup from open tasks

### 3. Design Workflow
- Added `original_requester_id` field to Task model
- When design team completes work, it automatically routes back to the editorial person who originally requested it
- Only design manager can override this workflow

### 4. Dashboard Improvements
- Dashboard shows only 5 recent todo tasks with "View All" link
- My Todo List page shows 20 tasks per page with pagination
- CXO dashboard cleaned up (removed All Tasks, All Magazines, All Todo list)
- Articles are now clickable in CXO dashboard and all articles page

## Database Setup

### Option 1: Fresh Setup (Recommended for New Environments)

```bash
# Run migrations to create all tables
python -c "from app import create_app; from flask_migrate import upgrade; app = create_app(); app.app_context().push(); upgrade()"

# Seed comprehensive data with all use cases
python seed_comprehensive_with_managers.py
```

### Option 2: Existing Database (When Database Already Exists)

```bash
# Stamp the database at the current revision
python -c "from app import create_app; from flask_migrate import stamp; app = create_app(); app.app_context().push(); stamp(revision='add_task_dept_mgr')"

# Clear and re-seed with comprehensive data
python seed_comprehensive_with_managers.py
```

## Test Users

The comprehensive seed data creates the following users:

### Admin
- **super_admin** (super_admin@magazine.com) - Super Administrator [MANAGER]

### Executive
- **ceo_john** (ceo@magazine.com) - CXO [MANAGER]
- **cmo_sarah** (cmo@magazine.com) - CXO

### Sales Department
- **sales_manager** (sales_mgr@magazine.com) - Sales Manager [MANAGER]
- **john_sales** (john@magazine.com) - Sales Representative
- **mary_sales** (mary@magazine.com) - Sales Representative

### Editorial Department
- **editorial_manager** (editorial_mgr@magazine.com) - Editorial Manager [MANAGER]
- **editor_jane** (jane@magazine.com) - Editor
- **editor_mike** (mike@magazine.com) - Editor
- **editor_lisa** (lisa@magazine.com) - Editor

### Design Department
- **design_manager** (design_mgr@magazine.com) - Design Manager [MANAGER]
- **designer_sarah** (sarah@magazine.com) - Designer
- **designer_david** (david@magazine.com) - Designer
- **designer_amy** (amy@magazine.com) - Designer

## Test Scenarios Included

The seed data includes 28+ tasks demonstrating:

1. **Task assigned to Editorial Department** - Goes to editorial_manager
2. **Editorial Manager assigns to team member** - Manager reassigns to editor_jane
3. **Task in Open state for Editorial pickup** - Available for any editorial team member
4. **Task sent to Design department** - Forwarded to design_manager
5. **Design team member working on task** - Assigned to designer_sarah
6. **Design completed - returning to Editorial** - Returns to original requester (editor_jane)
7. **Design open task for pickup** - Available for design team
8. **Multiple department handoffs** - Complex workflow demonstration
9. **20+ additional tasks** - For testing todo list pagination

## Brands & Editions

- 5 Brands created (Tech Magazine, Business Weekly, Lifestyle Monthly, etc.)
- 30 Editions created (6 months for each brand in 2025)

## CXO Articles

- 10 CXO articles with various statuses (Pending, Approved, Rejected)

## Verifying Setup

After running the seed script, you should see:
```
================================================================================
COMPREHENSIVE SEED DATA CREATED SUCCESSFULLY!
================================================================================

USERS:
--------------------------------------------------------------------------------
  14 users created with managers marked

DEPARTMENT WORKFLOW DEMONSTRATION:
--------------------------------------------------------------------------------
  ✓ Tasks assigned to department go to department manager
  ✓ Manager can reassign to team members
  ✓ Open tasks available for any team member to pickup
  ✓ Design team returns completed work to original editorial requester
  ✓ Only design manager can override this workflow

TODO LIST PAGINATION:
--------------------------------------------------------------------------------
  Total tasks for testing: 28
  Dashboard shows: 5 recent tasks with 'View All' link
  All Todo List shows: 20 tasks per page with pagination
```

## Migration Files

The database uses the following migration chain:

1. `9e4d1527b281` - Initial migration (Add new fields and CXOArticle model)
2. `c76bd2127030` - Add CXO article files table
3. `d8e3f520a9b2` - Add file deletion tracking
4. `add_task_dept_mgr` - Add task department and manager fields (NEW)

## Troubleshooting

### Migration Errors

If you encounter "Multiple head revisions" error:
```bash
# Check current migration status
python -c "from app import create_app; from flask_migrate import current; app = create_app(); app.app_context().push(); print(current())"

# Stamp to latest revision
python -c "from app import create_app; from flask_migrate import stamp; app = create_app(); app.app_context().push(); stamp(revision='add_task_dept_mgr')"
```

### Duplicate Column Errors

If you see "column already exists" errors, it means the database already has the schema. Just stamp it:
```bash
python -c "from app import create_app; from flask_migrate import stamp; app = create_app(); app.app_context().push(); stamp(revision='add_task_dept_mgr')"
```

### Verify Fields Exist

To verify the new fields are in the database:
```bash
python -c "from app import create_app, db; from app.models import User, Task; app = create_app(); app.app_context().push(); u = User.query.first(); t = Task.query.first(); print(f'is_manager: {hasattr(u, \"is_manager\")}'); print(f'assigned_department: {hasattr(t, \"assigned_department\")}'); print(f'original_requester_id: {hasattr(t, \"original_requester_id\")}')"
```

All three should return `True`.
