# Magazine Task Management System - Complete User Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [User Roles & Permissions](#user-roles--permissions)
3. [Login & Authentication](#login--authentication)
4. [Dashboard Overview](#dashboard-overview)
5. [Task Management](#task-management)
6. [Department-Specific Features](#department-specific-features)
7. [CXO Articles](#cxo-articles)
8. [Magazine Management](#magazine-management)
9. [Ads Management](#ads-management)
10. [Notifications](#notifications)
11. [FAQ & Troubleshooting](#faq--troubleshooting)

---

## Getting Started

### System Requirements
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection
- Login credentials provided by administrator

### Accessing the System
1. Navigate to the application URL
2. You'll see the login page
3. Enter your username and password
4. Click "Login" button

### First Login
- All test accounts use password: `password123`
- You'll be redirected to your role-specific dashboard
- Take a moment to explore the navigation menu

---

## User Roles & Permissions

### 1. Super Admin
**Access Level**: Full system access

**Capabilities**:
- View and manage all tasks across departments
- Create and manage brands
- Create and manage editions
- Assign tasks to any department
- Override any workflow
- Access all reports and analytics
- Manage users (view all users)

**Dashboard Features**:
- Complete system overview
- All department statistics
- System-wide task counts
- All notifications

---

### 2. CXO (Chief Experience Officer)
**Access Level**: Executive oversight

**Capabilities**:
- Upload and manage CXO articles
- View all articles across the organization
- Track article publication status
- Access executive dashboard
- View high-level analytics

**Dashboard Features**:
- Article overview
- Publication pipeline
- Quick upload functionality
- Article statistics

**Workflow**:
```
CXO Dashboard → Upload Article → Track Status → View Published Articles
```

---

### 3. Sales Department

#### Sales Manager
**Access Level**: Sales team oversight + Manager privileges

**Capabilities**:
- Create new tasks for editorial/design
- Assign tasks to sales team members
- View all sales department tasks
- Override task assignments within sales
- Mark tasks as Open for team pickup
- Communicate with editorial/design teams

#### Sales Team Member
**Access Level**: Assigned tasks + Open tasks

**Capabilities**:
- Create new tasks
- View assigned tasks
- Pick up open tasks in sales department
- Track task progress
- Upload files and add comments

**Typical Workflow**:
```
Create Task → Assign to Editorial → Editorial Works → Design Works → 
Sales Reviews → Client Feedback → Back to Editorial/Design → Final Approval
```

---

### 4. Editorial Department

#### Editorial Manager
**Access Level**: Editorial oversight + Manager privileges

**Capabilities**:
- View all editorial tasks
- Assign tasks to editorial team members
- Create ownership for repeating workflows
- Send tasks to design or sales
- Override task assignments
- Mark tasks as Open for team pickup

#### Editorial Team Member
**Access Level**: Assigned tasks + Open tasks

**Capabilities**:
- View assigned tasks
- Pick up open editorial tasks
- Edit content and upload files
- Send completed work to design
- Send completed work back to sales
- Request feedback from manager
- Add comments and track history

**Typical Workflow**:
```
Receive from Sales → Edit Content → Send to Design → 
Receive from Design → Review → Send to Sales/Design (loop possible)
```

**Important**: When you send a task to design:
- **First time**: Goes to Design Manager
- **After manager assigns designer**: Future sends go directly to that designer
- **Loop**: The same designer will receive the task every time you send it back

---

### 5. Design Department

#### Design Manager
**Access Level**: Design oversight + Manager privileges

**Capabilities**:
- View all design tasks
- Assign tasks to design team members
- Create ownership for repeating workflows
- Override designer assignments
- Mark tasks as Open for team pickup
- Complete tasks without returning to editorial

#### Design Team Member
**Access Level**: Assigned tasks + Open tasks

**Capabilities**:
- View assigned tasks
- Pick up open design tasks
- Create designs and upload files
- Send completed work back to editorial
- Add design comments
- Track design iterations

**Typical Workflow**:
```
Receive from Editorial → Create Design → Send Back to Editorial → 
Receive Feedback → Revise → Send Back (loop continues)
```

**Loop Behavior**: Once you're assigned to a task:
- Editorial will send the task directly to YOU
- Not to the Design Manager
- This continues until manager reassigns

---

## Login & Authentication

### Login Page Features

1. **Username Field**
   - Enter your username
   - Or use the dropdown to quick-select

2. **Quick Select Dropdown**
   - Browse users by department
   - Click to auto-fill username field
   - Shows manager status

3. **Password Field**
   - Default password: `password123`
   - Contact admin to change password

4. **Login Button**
   - Click to access the system
   - You'll be redirected to your dashboard

### Test Account Credentials

| Department | Username | Role | Password |
|------------|----------|------|----------|
| Admin | super_admin | Super Admin | password123 |
| Executive | ceo_john | CEO | password123 |
| Executive | cmo_sarah | CMO | password123 |
| Sales | sales_manager | Manager | password123 |
| Sales | john_sales | Team Member | password123 |
| Sales | mary_sales | Team Member | password123 |
| Editorial | editorial_manager | Manager | password123 |
| Editorial | editor_jane | Team Member | password123 |
| Editorial | editor_mike | Team Member | password123 |
| Editorial | editor_lisa | Team Member | password123 |
| Design | design_manager | Manager | password123 |
| Design | designer_sarah | Team Member | password123 |
| Design | designer_david | Team Member | password123 |
| Design | designer_amy | Team Member | password123 |

---

## Dashboard Overview

### Navigation Menu

All users see:
- **Dashboard**: Your home page
- **My Tasks**: Tasks assigned to you
- **All Tasks**: All tasks you can view
- **Create Task**: Create new task
- **Brands**: Manage brands (Admin)
- **Editions**: Manage editions
- **Profile**: Your user info
- **Logout**: Sign out

Additional for specific roles:
- **CXO**: Articles, Upload Article
- **Admin**: Open Tasks, Ads

### Dashboard Sections

#### 1. Welcome Message
- Displays your name and role
- Shows current date/time

#### 2. Department Overview (Sales/Editorial/Design)
- **Assigned to Me**: Your active tasks
- **Department Total**: All department tasks
- **Completed**: Finished tasks
- **In Progress**: Active work

#### 3. Recent Tasks (Top 5)
- Latest task updates
- Status indicators
- Quick actions
- "View All" link to My Tasks

#### 4. Quick Stats
- Priority breakdown
- Department distribution
- Status overview

#### 5. Notifications
- Recent alerts
- Task assignments
- Status changes
- Unread count

---

## Task Management

### Creating a Task

#### Step 1: Click "Create Task"

#### Step 2: Fill Task Details

**Basic Information**:
- **Brand**: Select magazine brand (required)
- **Edition**: Select specific edition (required)
- **Or Enter Edition Manually**: For non-listed editions

**Task Details**:
- **Title**: Brief task description
- **Company Name**: Client/subject name (required)
- **Company URL**: Website link (optional)
- **Category**: Select type (Profile, Article, Cover, AD, etc.)
- **Or Enter Category Manually**: For other types

**Content**:
- **Description**: Detailed task description (required)
- **Deadline**: Due date (required)
- **Priority**: Low / Normal / High (required)

**Assignment**:
- **Assign to Department**: Editorial / Design / Sales
- Status automatically set based on assignment

**Files**:
- **Upload Files**: Attach relevant documents
- Supported: PDF, Images, Documents, Audio, Video
- Max size: 50MB per file

#### Step 3: Click "Create Task"

Task is created and assigned!

---

### Viewing Tasks

#### My Tasks Page

**What You See**:
- Tasks assigned to you
- Current status
- Priority level
- Deadline
- Action buttons

**Filtering**:
- Search by company name or description
- Filter by brand
- Filter by priority
- Filter by category

**Actions Available**:
- **View**: See full task details
- **Mark Complete**: Finish task (if applicable)
- **Send Back**: Return to sender
- **Send to Design**: Forward to design (editorial)
- **Send to Sales**: Send to sales (editorial)

---

### Task Detail Page

#### Information Displayed

1. **Task Header**
   - Task ID and Title
   - Status badge (color-coded)
   - Priority indicator
   - Brand and Edition

2. **Task Information**
   - Company Name and URL
   - Category
   - Description
   - Created by
   - Assigned to
   - Current Department
   - Deadlineand Dates

3. **Task Actions** (Role-dependent)
   - Mark as Complete
   - Send to Editorial
   - Send to Design
   - Send to Sales
   - Send Back to Manager
   - Assign to Team Member (Managers only)
   - Archive Task

4. **Files Section**
   - All uploaded files
   - Download links
   - Upload new files
   - File history

5. **Comments Section**
   - Add comments
   - View comment history
   - Timestamps and authors

6. **Task History**
   - Complete audit trail
   - All status changes
   - Department transfers
   - Assignments
   - File uploads
   - Comments

---

### Task Actions Explained

#### 1. Mark as Complete
**Who Can Use**: Anyone assigned to the task

**What Happens**:
- **Design Team Member**: Returns to editorial requester
- **Editorial Team Member**: Task marked complete
- **Sales**: Task marked complete
- **Managers**: Can complete without returning

**Steps**:
1. Click "Mark as Complete"
2. Add optional comment
3. Confirm action
4. Task moves to appropriate next step

---

#### 2. Send to Design
**Who Can Use**: Editorial users

**What Happens**:
- **First time**: Goes to Design Manager
- **After designer assigned**: Goes directly to assigned designer
- Creates "design owner" for this task

**Steps**:
1. Click "Send to Design"
2. Add comment (optional)
3. Task moves to design department

---

#### 3. Send Back to Editorial
**Who Can Use**: Design users

**What Happens**:
- Returns to editorial owner (the person who sent it)
- Creates a loop between designer and editor
- Maintains ownership for repeated sends

**Steps**:
1. Click "Send Back to Editor"
2. Add comment with feedback
3. Task returns to editorial

---

#### 4. Send to Sales
**Who Can Use**: Editorial users

**What Happens**:
- Returns to original sales person (task creator)
- Used for client feedback
- Can be sent back to editorial

**Steps**:
1. Click "Send to Sales"
2. Add comment
3. Sales person reviews

---

#### 5. Assign to Team Member
**Who Can Use**: Managers only

**What Happens**:
- Sets ownership for the department
- Future tasks in this loop return to this person
- Can be changed by manager (override)

**Steps**:
1. Click "Assign to Team Member"
2. Select team member from dropdown
3. Click "Assign"
4. Team member receives notification

---

#### 6. Send Back to Manager
**Who Can Use**: Team members

**What Happens**:
- Returns task to department manager
- Used when help needed
- Manager can reassign or assist

**Steps**:
1. Click "Send Back to Manager"
2. Add comment explaining issue
3. Manager receives task

---

### Open Tasks

**What Are Open Tasks?**
- Tasks not assigned to specific person
- Available for anyone in department to pick up
- Created when manager marks task as "Open"

**How to Pick Up**:
1. Go to "Open Tasks" (in menu)
2. Browse available tasks
3. Click "Pick Up Task"
4. Task is now assigned to you

**When to Use**:
- Distribute workload evenly
- Allow team to choose tasks
- Emergency/urgent tasks

---

## Department-Specific Features

### Sales Department Workflows

#### Creating Client Tasks
```
New Client → Create Task → Choose Editorial → 
Add Details → Upload Brief → Submit
```

#### Reviewing Completed Work
```
Receive Notification → Review Task → 
Client Feedback → Send to Editorial or Approve
```

#### Managing Client Revisions
```
Client Wants Changes → Add Comment → 
Send Back to Editorial → Track Progress
```

---

### Editorial Department Workflows

#### Content Creation Flow
```
Receive Task → Research → Write Content → 
Upload Draft → Need Design? → Send to Design
```

#### Design Review Loop
```
Receive from Design → Review Design → 
Approve or Request Changes → Send Back to Design or Sales
```

#### The Editorial-Design Loop
**Scenario**: Jane (editorial) working with Sarah (design)

**First Time**:
1. Sales creates task → Editorial Manager
2. Manager assigns to Jane (Jane becomes editorial owner)
3. Jane sends to design → Design Manager
4. Manager assigns to Sarah (Sarah becomes design owner)

**The Loop**:
5. Sarah completes → Automatically goes to Jane
6. Jane requests change → Automatically goes to Sarah
7. Sarah revises → Automatically goes to Jane
8. Repeat until approved

**Loop continues between Jane ↔ Sarah forever until**:
- Jane sends to Sales (task complete)
- Manager reassigns to different designer/editor
- Task is archived

---

### Design Department Workflows

#### Design Creation
```
Receive Task → Review Requirements → 
Create Design → Upload Files → Send to Editorial
```

#### Revision Process
```
Receive Feedback → Review Comments → 
Revise Design → Upload New Version → Send Back
```

#### Direct Designer Assignment
Once assigned to a task by manager:
- All future sends from editorial come to YOU
- No need for manager intermediary
- Loop established until manager changes it

---

## CXO Articles

### Uploading Articles

#### Step 1: Navigate to "Upload Article"

#### Step 2: Fill Article Details
- **Title**: Article headline
- **Content**: Full article text
- **Author**: Your name or article author
- **Publication Date**: When to publish
- **Related Task**: Link to task (optional)

#### Step 3: Upload Files
- Featured image
- Supporting documents
- Media files

#### Step 4: Submit

### Managing Articles

**View All Articles**:
- All CXO articles
- Publication status
- Edit/Delete options

**Article Status**:
- Draft
- Published
- Archived

**Actions**:
- Edit article
- Change publication date
- Archive article
- Link to task

---

## Magazine Management

### Brands

**What Are Brands?**
- Magazine titles (e.g., "Tech Magazine", "Business Weekly")
- Container for editions
- Assigned to tasks

**Creating a Brand** (Admin only):
1. Go to "Brands"
2. Click "Create New Brand"
3. Enter:
   - Name (required, unique)
   - Description
4. Click "Create Brand"

**Managing Brands**:
- View all brands
- See editions count
- Edit brand details
- Delete brand (if no editions)

---

### Editions

**What Are Editions?**
- Specific magazine issues
- Linked to brands
- Have year/month
- Track status

**Creating an Edition**:
1. Go to "Editions"
2. Click "Create New Edition"
3. Select:
   - Brand (required)
   - Year (required)
   - Month (required)
   - Name/Title
4. Set Status:
   - Scheduled
   - Ongoing
   - Completed
5. Click "Create Edition"

**Edition Detail Page**:
- All tasks for this edition
- Task statistics
- Timeline view
- Quick task creation

---

## Ads Management

### Viewing Ads
- See all uploaded advertisements
- Filter by brand
- Search by title or notes

### Uploading Ads
1. Go to "Ads"
2. Click "Upload Ad"
3. Fill details:
   - Brand
   - Title
   - Ad Size
   - Client Name
   - Upload file (image/PDF)
   - Notes
4. Click "Upload"

### Managing Ads
- View ad preview
- Edit ad details
- Delete ad
- Download ad file

---

## Notifications

### How Notifications Work

**You Receive Notifications When**:
- Task assigned to you
- Task status changes
- Someone comments on your task
- Manager sends you a task
- Design/Editorial sends you a task

### Notification Badge
- Red number in navigation
- Shows unread count
- Clickable to view all

### Viewing Notifications
1. Click notification badge
2. See list of all notifications
3. Click notification to go to task
4. Notifications mark as read

---

## FAQ & Troubleshooting

### Common Questions

**Q: How do I change my password?**
A: Contact system administrator. Self-service password change coming soon.

**Q: Can I delete a task?**
A: Only administrators can delete tasks. You can archive tasks instead.

**Q: Why did my task go to the manager instead of my team member?**
A: First-time assignments go to managers. After manager assigns, subsequent sends go directly to the assigned person.

**Q: How do I know who will receive my task?**
A: Check the task detail page - it shows the current owner for each department.

**Q: Can I upload multiple files?**
A: Yes! You can upload multiple files at once or add files later.

**Q: What if I pick up the wrong open task?**
A: Send it back to your manager who can reassign it.

**Q: How do I see all my department's tasks?**
A: Go to "All Tasks" and filter by your department.

**Q: Why can't I see design tasks?** (Editorial user asking)
A: Cross-department viewing is limited. You see tasks when they're assigned to you.

**Q: How do I break the editorial-design loop?**
A: Editorial user can "Send to Sales" to complete the task.

**Q: Can a manager reassign a task in the middle of a loop?**
A: Yes! Managers can always override and assign to a different team member.

### Troubleshooting

**Problem: Can't login**
- Verify username is correct (case-sensitive)
- Try default password: password123
- Clear browser cache
- Try different browser

**Problem: Don't see my tasks**
- Check "My Tasks" not "All Tasks"
- Verify tasks are assigned to you
- Check filters aren't hiding tasks
- Refresh the page

**Problem: Can't upload files**
- Check file size (max 50MB)
- Verify file type is supported
- Try smaller file
- Check internet connection

**Problem: Task went to wrong person**
- Check task history
- Manager may have reassigned
- Contact manager to fix

**Problem: Notifications not showing**
- Refresh page
- Check notification badge number
- Clear browser cache

**Problem: Can't complete task**
- Verify task is assigned to you
- Check you have permission for this action
- See if task is already completed

---

## Best Practices

### For Sales Team
1. Provide clear task descriptions
2. Upload client briefs and requirements
3. Set realistic deadlines
4. Communicate client feedback clearly
5. Review work promptly

### For Editorial Team
1. Read requirements carefully
2. Upload drafts for review
3. Use comments for questions
4. Send to design when content is finalized
5. Review design feedback thoroughly

### For Design Team
1. Review editorial content before designing
2. Upload design iterations
3. Use comments to explain design choices
4. Respond to feedback requests quickly
5. Keep file versions organized

### For Managers
1. Assign tasks fairly across team
2. Monitor team workload
3. Set clear expectations
4. Respond to escalations quickly
5. Override only when necessary

### For Everyone
1. Check notifications daily
2. Update task status regularly
3. Add meaningful comments
4. Upload files with clear names
5. Meet deadlines
6. Communicate proactively
7. Use task history to understand context

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Alt + D | Go to Dashboard |
| Alt + T | Go to My Tasks |
| Alt + C | Create New Task |
| Alt + N | View Notifications |
| Alt + L | Logout |

---

## Getting Help

**Technical Issues**:
- Contact IT support
- Check system status
- Submit bug report

**Workflow Questions**:
- Ask your manager
- Review this guide
- Contact admin

**Feature Requests**:
- Submit feedback
- Contact admin
- Team meetings

---

**Last Updated**: November 2025
**Version**: 1.0.0

---

## Quick Reference Cards

### Sales Quick Reference
```
CREATE TASK → Choose Department → Add Details → Upload Files → Submit
REVIEW WORK → Check Quality → Client Feedback → Send Back or Approve
```

### Editorial Quick Reference
```
RECEIVE TASK → Create Content → Upload Draft → Send to Design
REVIEW DESIGN → Approve or Request Changes → Send Back or Forward
```

### Design Quick Reference
```
RECEIVE TASK → Create Design → Upload Files → Send to Editorial
REVISE → Review Feedback → Update Design → Send Back
```

### Manager Quick Reference
```
ASSIGN TASK → Select Team Member → Set Owner → Monitor Progress
OVERRIDE → Reassign if Needed → Help Team → Resolve Issues
```

---

*This guide is continuously updated. Please check back regularly for new features and updates.*
