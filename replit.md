# Magazine Task Management System

## Overview
This project is a comprehensive multi-department task management web application designed for magazine production companies. It streamlines workflows across Sales, Editorial, and Design departments, integrating brand and edition tracking. The system enhances efficiency, collaboration, and oversight in the magazine production process. Key capabilities include flexible task assignment, a robust task pickup system, CXO article lifecycle management, and detailed audit trails. The business vision is to provide a central platform for managing the entire magazine production pipeline, reducing bottlenecks and improving communication, ultimately leading to faster production cycles and higher-quality output.

## User Preferences
- I prefer simple language.
- I want iterative development.
- Ask before making major changes.
- I prefer detailed explanations.
- Do not make changes to the folder Z.
- Do not make changes to the file Y.

## System Architecture
The application is built on a Flask framework, employing a modular structure with blueprints for different functionalities like authentication, main dashboard, tasks, magazines, and ads. SQLAlchemy serves as the ORM, with PostgreSQL as the primary database and SQLite as a fallback. The frontend utilizes Bootstrap 5 for a responsive design and vanilla JavaScript for interactivity. File storage is managed locally.

### UI/UX Decisions
- **Responsive Design**: Implemented with Bootstrap 5 for optimal viewing across devices.
- **Consistent Task Display**: Reusable Jinja2 macros ensure a uniform look for tasks throughout the application.
- **Dashboard Design**: Dashboards are tailored to department-specific needs, particularly article-focused for CXO users.
- **Pagination**: Implemented for efficient navigation through extensive lists.

### Technical Implementations
- **Authentication**: Role-based access control (RBAC) with distinct roles (Sales, Editorial, Design, Manager, Super Admin) and an `is_manager` flag.
- **Database Migrations**: Managed with Flask-Migrate (Alembic) for schema evolution.
- **Comprehensive Seed Data**: Includes users, brands, editions, tasks, CXO articles, and history for robust testing and demonstration.
- **Soft Deletion**: Implemented for task files, with deletion tracking visible only to Super Admins.

### Feature Specifications
- **Flexible Task Workflow**: Tasks can be assigned to any department without restriction and can flow freely between them.
- **Department-Based Task Routing**: Tasks are assigned to departments, with automatic routing to department managers by default.
- **Task Pickup System**: Users can pick up unassigned tasks, and managers can assign tasks to team members.
- **Personalized Todo Lists**: "My Todo List" displays tasks specifically assigned to the current user.
- **CXO Article Workflow**: Supports article submission, editorial review (approve/reject), automatic design task creation on approval, and lifecycle management (marking as "Used").
- **Task History & File Management**: Provides a complete audit trail of task actions and attached files, with files linked to specific history entries.
- **Advanced Filtering and Search**: Implemented across all major pages for efficient data retrieval.
- **Notifications**: System-generated notifications for task assignments, status changes, and article updates.

### System Design Choices
- **Modular Application Structure**: Blueprints organize routes and logic by feature for maintainability and scalability.
- **Fallback Database**: Configured SQLite for development and environments where PostgreSQL is unavailable.
- **Workflow Flexibility**: Tasks are primarily assigned to departments, with managers able to reassign to individuals or open pools.
- **Original Requester Tracking**: Ensures design tasks return to the correct editorial contact upon completion.
- **Manager Oversight**: Department managers have comprehensive dashboards for workload tracking and task assignment.
- **Automatic CXO Article Status & Assignment Synchronization**: CXO article status and assignment automatically update based on linked task status and department.
- **CXO Manager Edit Functionality**: CXO managers can edit unused CXO articles, with changes logged.
- **Simplified CXO Department Sidebar**: Navigation is streamlined for CXO users, focusing on article and ad management.
- **Design Department Enhancements**: All design users can view CXO articles, and design managers can create tasks and assign them.
- **Editorial Department Permissions**: Editorial team can access all CXO articles, and only editorial managers can create tasks.

## External Dependencies
- **Backend Framework**: Flask 3.x
- **Database**: PostgreSQL (primary), SQLite (fallback)
- **ORM**: SQLAlchemy
- **Database Migrations**: Flask-Migrate
- **Frontend Framework**: Bootstrap 5
- **JavaScript**: Vanilla JavaScript