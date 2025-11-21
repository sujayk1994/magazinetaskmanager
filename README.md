# Magazine Task Management System

A comprehensive task management system designed for magazine publishing workflows across Sales, Editorial, and Design departments.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.11-green.svg)
![Flask](https://img.shields.io/badge/flask-3.0.0-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Login Credentials](#login-credentials)
- [Documentation](#documentation)
- [Technology Stack](#technology-stack)
- [Deployment](#deployment)
- [Support](#support)

---

## 🎯 Overview

Magazine Task Management System streamlines the workflow between Sales, Editorial, and Design teams for magazine content creation and publication. It provides role-based access control, automated task routing, and comprehensive audit trails.

### Key Capabilities

- **Role-Based Workflows**: Different permissions for Sales, Editorial, Design, CXO, and Admin
- **Smart Task Routing**: Automatic assignment based on ownership and department rules
- **Loop Management**: Efficient editorial-design collaboration cycles
- **File Management**: Upload and version tracking for all task-related files
- **CXO Articles**: Dedicated module for executive content management
- **Magazine Management**: Brands and editions organization
- **Ads Management**: Advertisement upload and tracking
- **Real-Time Notifications**: Stay updated on task changes and assignments

---

## ✨ Features

### 🔐 Authentication & Authorization
- Secure password-based login
- Role-based access control (RBAC)
- Session management
- Department-specific permissions

### 📊 Task Management
- Create and assign tasks across departments
- Track task status and progress
- File uploads and versioning
- Comment system for collaboration
- Complete audit trail with history tracking
- Priority levels (Low, Normal, High)
- Multiple task categories

### 🔄 Workflow Automation
- **Smart Routing**: Tasks automatically route to the right person
- **Ownership System**: Once assigned, future tasks go directly to the owner
- **Loop Management**: Efficient editorial ↔ design collaboration
- **Manager Override**: Managers can reassign and change ownership
- **Open Tasks**: Team members can pick up unassigned tasks

### 👥 Department Features

**Sales**:
- Create client tasks
- Monitor progress
- Client feedback management

**Editorial**:
- Content creation and editing
- Send to design/sales
- Review design work

**Design**:
- Design creation
- Iterative feedback loops
- Direct collaboration with editorial

**CXO**:
- Article management
- Publication tracking
- Executive dashboard

**Admin**:
- Full system access
- Brand and edition management
- User oversight

### 📁 Additional Modules
- **Brands**: Magazine title management
- **Editions**: Issue tracking and organization
- **Ads**: Advertisement upload and management
- **Notifications**: Real-time alerts for task changes
- **Reports**: Task statistics and analytics

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+ (or use Replit's built-in database)
- Modern web browser

### Installation on Replit (Recommended)

1. **Fork or Clone** this Repl
2. **Run the application**:
   ```bash
   python main.py
   ```
3. **Seed test data**:
   ```bash
   python seed_comprehensive_with_managers.py
   ```
4. **Access** the application:
   - Open the webview in Replit
   - Navigate to the login page

### Local Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd magazine-task-management
   ```

2. **Create virtual environment**:
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**:
   ```bash
   export DATABASE_URL="postgresql://user:password@localhost/magazine_app"
   export SESSION_SECRET="your-random-secret-key"
   ```

5. **Initialize database**:
   ```bash
   python seed_comprehensive_with_managers.py
   ```

6. **Run the application**:
   ```bash
   python main.py
   ```

7. **Open browser**:
   ```
   http://localhost:5000
   ```

---

## 🔑 Login Credentials

All test accounts use the same password for easy team testing.

### Default Credentials

**Password for all users**: `password123`

### Test Accounts by Department

| Department | Username | Role | Description |
|------------|----------|------|-------------|
| **Administration** |
| Admin | `super_admin` | Super Admin | Full system access |
| **Executive** |
| Executive | `ceo_john` | CEO | CXO dashboard and articles |
| Executive | `cmo_sarah` | CMO | CXO features |
| **Sales** |
| Sales | `sales_manager` | Manager | Team oversight |
| Sales | `john_sales` | Team Member | Sales tasks |
| Sales | `mary_sales` | Team Member | Sales tasks |
| **Editorial** |
| Editorial | `editorial_manager` | Manager | Team oversight |
| Editorial | `editor_jane` | Team Member | Content editing |
| Editorial | `editor_mike` | Team Member | Content editing |
| Editorial | `editor_lisa` | Team Member | Content editing |
| **Design** |
| Design | `design_manager` | Manager | Team oversight |
| Design | `designer_sarah` | Team Member | Design work |
| Design | `designer_david` | Team Member | Design work |
| Design | `designer_amy` | Team Member | Design work |

### Quick Login Guide

1. Navigate to the login page
2. **Option 1**: Enter username and password manually
3. **Option 2**: Use the dropdown to quick-select a user
4. Click "Login"

---

## 📚 Documentation

Comprehensive documentation is available in the following files:

### User Documentation
- **[USER_GUIDE.md](USER_GUIDE.md)** - Complete user guide covering:
  - Getting started
  - Role-specific features
  - Task management workflows
  - Step-by-step instructions
  - FAQ and troubleshooting

### Technical Documentation
- **[TECHNICAL_DOCUMENTATION.md](TECHNICAL_DOCUMENTATION.md)** - Technical reference covering:
  - System architecture
  - Database schema
  - Routing logic and algorithms
  - Task ownership system
  - API endpoints
  - Security considerations

### Deployment Documentation
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Deployment instructions for:
  - Replit deployment (recommended)
  - Docker deployment
  - Manual server deployment
  - Environment configuration
  - Database setup
  - Troubleshooting

### Additional Documentation
- **[TASK_ROUTING_LOGIC.md](TASK_ROUTING_LOGIC.md)** - Detailed explanation of the task routing system

---

## 🛠 Technology Stack

### Backend
- **Python 3.11** - Programming language
- **Flask 3.0** - Web framework
- **SQLAlchemy** - ORM
- **PostgreSQL 15** - Database
- **Flask-Migrate** - Database migrations
- **Werkzeug** - Password hashing
- **Gunicorn** - WSGI server (production)

### Frontend
- **Jinja2** - Template engine
- **Bootstrap 5** - CSS framework
- **Bootstrap Icons** - Icon library
- **JavaScript** - Client-side interactivity

### Deployment
- **Replit** - Primary hosting platform
- **Docker** - Containerization (alternative)
- **Nginx** - Reverse proxy (manual deployment)

---

## 🌐 Deployment

### Replit Deployment (Recommended)

The application is optimized for Replit deployment with autoscale configuration.

1. Click the **Deploy** button in Replit
2. Set environment variables in the Secrets tab
3. Application will autoscale based on traffic

**Benefits**:
- Automatic scaling
- Built-in PostgreSQL
- Zero configuration
- Cost-effective (only runs when needed)

### Docker Deployment

For deployment on other platforms:

```bash
# Using Docker Compose
docker-compose up -d

# Initialize database
docker-compose exec web python seed_comprehensive_with_managers.py

# Access at http://localhost:5000
```

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

---

## 📖 How It Works

### The Task Workflow

```mermaid
graph LR
    A[Sales Creates Task] --> B[Editorial Manager]
    B --> C[Editorial Team Member]
    C --> D[Design Manager]
    D --> E[Design Team Member]
    E --> C
    C --> E
    E --> C
    C --> F[Back to Sales]
```

### Key Concepts

#### 1. First-Time Routing
- Tasks initially go to **department managers**
- Manager assigns to specific team member
- **Ownership is established**

#### 2. The Loop System
Once ownership is established:
- Editorial sends to design → Goes to **assigned designer**
- Designer sends back → Goes to **assigned editor**
- Loop continues: Editor ↔ Designer

#### 3. Manager Override
- Managers can **reassign** at any time
- New assignment **updates ownership**
- Loop now includes new person

Example:
```
Sales John creates task
  → Editorial Manager assigns to Jane [Jane becomes owner]
  → Jane sends to design
  → Design Manager assigns to Sarah [Sarah becomes owner]
  → Sarah sends back → Jane
  → Jane sends to design → Sarah
  → Loop: Jane ↔ Sarah (repeats until complete)
```

If manager reassigns Sarah to Amy:
```
  → New loop: Jane ↔ Amy
```

---

## 🎨 Features Demonstration

### Creating a Task

```
1. Sales user logs in
2. Clicks "Create Task"
3. Fills in:
   - Brand and Edition
   - Company name
   - Description
   - Assign to Editorial
4. Uploads client brief
5. Submits
→ Task created and assigned to Editorial Manager
```

### Editorial-Design Collaboration

```
1. Editorial Manager assigns to Jane
2. Jane writes content and sends to Design
3. Design Manager assigns to Sarah
4. Sarah creates design and sends back
5. Jane reviews and requests changes
6. Sarah receives (directly, not via manager)
7. Sarah revises and sends back
8. Jane approves and sends to Sales
→ Client reviews final product
```

### Picking Up Open Tasks

```
1. Manager marks task as "Open"
2. Any team member can view in "Open Tasks"
3. Team member clicks "Pick Up Task"
4. Task is assigned to them
→ Workload distributed flexibly
```

---

## 📊 Project Statistics

- **14 Test Users** across all departments
- **5 Brands** with **30 Editions**
- **28 Sample Tasks** demonstrating all workflows
- **10 CXO Articles** for content management
- **Complete Audit Trail** for every action
- **File Upload Support** for all task types

---

## 🔒 Security Features

- ✅ Password hashing with Werkzeug
- ✅ Session-based authentication
- ✅ Role-based access control (RBAC)
- ✅ SQL injection prevention (ORM)
- ✅ File upload validation
- ✅ CSRF protection
- ✅ Secure file storage

---

## 🧪 Testing

### Manual Testing

All workflows have been tested:
- ✅ User authentication
- ✅ Task creation and assignment
- ✅ Department routing
- ✅ Manager override
- ✅ Editorial-design loop
- ✅ File uploads
- ✅ Notifications
- ✅ CXO articles
- ✅ Ads management

### Test Data

Run the seed script to populate test data:
```bash
python seed_comprehensive_with_managers.py
```

This creates realistic scenarios for all workflows.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add comments for complex logic
- Write clear commit messages

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🆘 Support

### Getting Help

- **User Guide**: See [USER_GUIDE.md](USER_GUIDE.md)
- **Technical Docs**: See [TECHNICAL_DOCUMENTATION.md](TECHNICAL_DOCUMENTATION.md)
- **Deployment**: See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- **Issues**: Open an issue on GitHub

### Common Issues

**Can't login?**
- Verify username (case-sensitive)
- Use default password: `password123`
- Clear browser cache

**Tasks not routing correctly?**
- Check task history for ownership
- Verify department managers are assigned
- Review [TASK_ROUTING_LOGIC.md](TASK_ROUTING_LOGIC.md)

**Files won't upload?**
- Check file size (max 50MB)
- Verify file type is allowed
- Ensure stable internet connection

---

## 🗺️ Roadmap

### Planned Features

- [ ] Real-time notifications (WebSocket)
- [ ] Email notifications
- [ ] Advanced search and filters
- [ ] Analytics dashboard
- [ ] Mobile app
- [ ] REST API
- [ ] Task templates
- [ ] Recurring tasks
- [ ] Team chat integration

---

## 👨‍💻 Authors

Development Team - Magazine Task Management System

---

## 🙏 Acknowledgments

- Bootstrap for the UI framework
- Flask community for excellent documentation
- Replit for the deployment platform

---

## 📧 Contact

For questions or support, please contact the system administrator.

---

**Version**: 1.0.0  
**Last Updated**: November 2025  
**Status**: Production Ready ✅

---

## 🖼️ Screenshots

*Coming soon: Dashboard views, task workflows, and feature demonstrations*

---

**Made with ❤️ for efficient magazine publishing workflows**
