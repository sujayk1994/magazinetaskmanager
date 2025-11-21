# 📱 MAGAZINE TASK MANAGEMENT APP - COMPLETE WORKFLOW GUIDE

## 🎯 WHAT IS THIS APP?

This is a **Magazine Production Management System** that helps coordinate work between three departments:
- **Sales** - Uploads CXO articles from clients
- **Editorial** - Reviews and approves articles
- **Design** - Creates designs for approved articles

Think of it like an assembly line for magazine content, where each department has specific roles and tasks automatically flow between them.

---

## 🔑 LOGIN CREDENTIALS (For Testing)

| Username | Role | Department | Is Manager? |
|----------|------|------------|-------------|
| super_admin | Super Admin | admin | Yes |
| ceo_john | CXO | executive | Yes |
| sales_manager | Sales | sales | Yes |
| john_sales | Sales | sales | No |
| editorial_manager | Editorial | editorial | Yes |
| editor_jane | Editorial | editorial | No |
| design_manager | Design | design | Yes |
| designer_sarah | Design | design | No |

**Note:** There's NO password! Just select a username from the dropdown and click login.

---

## 📋 CXO ARTICLE WORKFLOW (The Main Flow)

### **SCENARIO 1: Article Gets Approved WITH Design Work**

```
1. Sales User (john_sales) logs in
   ↓
2. Uploads CXO article for "Tech Company"
   - Fills in company details
   - Uploads files (contract, logo, etc.)
   - Article Status: PENDING
   ↓
3. Editorial Manager (editorial_manager) receives notification
   ↓
4. Reviews article, clicks "Approve Article"
   ✓ CHECKS the "Create Design Task" checkbox ← IMPORTANT!
   - Article Status: APPROVED → AWAITING DESIGN
   - NEW task created for Design department
   - Task goes to "All Open Tasks" (NOT assigned to anyone)
   - All design team members get notification
   ↓
5. Designer (designer_sarah) sees task in "All Open Tasks"
   ↓
6. Clicks "Pick Up Task"
   - Article Status: DESIGNING
   - Task now in their "My Todo List"
   - Works on design, uploads design files
   ↓
7. Clicks "Mark as Complete"
   - Task automatically RETURNS to Editorial
   - Article Status: DESIGN READY
   - Editorial manager gets notified
   ↓
8. Editorial manager reviews design
   - If good: Marks task as complete
   - If changes needed: Reassigns back to design
   ↓
9. Editorial manager clicks "Mark as Used"
   - Article Status: USED
   - WORKFLOW COMPLETE! ✅
```

**KEY POINT:** The article flows: Pending → Approved → Awaiting Design → Designing → Design Ready → Used

**IMPORTANT:** Design tasks go directly to **Open Tasks** so ANY designer can pick them up (fair distribution)!

---

### **SCENARIO 2: Article Gets Approved WITHOUT Design Work**

```
1. Sales uploads article (same as above)
   ↓
2. Editorial reviews and clicks "Approve"
   ✗ UNCHECKS "Create Design Task" ← Article doesn't need design
   - Article Status: APPROVED
   - NO design task created
   ↓
3. Editorial clicks "Mark as Used" later
   - Article Status: USED
   - DONE! ✅
```

**KEY POINT:** Not all articles need design. The checkbox lets editorial decide.

---

### **SCENARIO 3: Article Gets Rejected**

```
1. Sales uploads article
   ↓
2. Editorial reviews and finds problems
   ↓
3. Clicks "Reject Article"
   - Must enter rejection reason
   - Article Status: REJECTED
   - Sales user gets notification with reason
   ↓
4. WORKFLOW ENDS (rejected articles cannot be edited)
```

---

## 🎨 DESIGN DEPARTMENT SPECIAL LOGIC

### **The "Return to Editorial" Rule**

When a **regular designer** (not a manager) completes a task that came from Editorial:

```
Designer clicks "Mark as Complete"
↓
Task DOES NOT complete!
Instead, it:
- Returns to Editorial department
- Gets assigned to the original editor who created it
- Status becomes "Review"
- Editorial must approve before final completion
```

**WHY?** Ensures editorial reviews and approves design work before considering it done.

### **Manager Override**

When a **Design Manager** completes the same task:
```
Design Manager clicks "Mark as Complete"
↓
Task is COMPLETED immediately
- Does NOT return to editorial
- Manager has authority to finalize
```

---

## 📊 OPEN TASKS SYSTEM

### **What Are "Open Tasks"?**

Tasks that are:
- In your department
- NOT assigned to anyone specific
- Available for anyone in the department to pick up

### **How It Works:**

```
Manager creates task for Editorial department
↓
Task auto-assigned to Editorial Manager
↓
Manager clicks "Assign to Team"
↓
Task becomes "Open" (assigned_to = None)
↓
Any editorial team member can see it in "All Open Tasks"
↓
Someone clicks "Pick Up Task"
↓
Task instantly assigned to them
↓
Appears in their "My Todo List"
```

**BENEFIT:** Distributes work fairly - whoever has time can grab the task.

---

## 👔 MANAGER WORKFLOWS

### **Manager Dashboard Shows:**

1. **Department Statistics**
   - Total tasks
   - Open tasks (available for pickup)
   - High/urgent priority counts

2. **Team Workload**
   - Each team member's name
   - How many active tasks they have
   - Helps balance work distribution

3. **Department Tasks**
   - All tasks in your department
   - Quick assign buttons

4. **Pending Articles** (Editorial managers only)
   - CXO articles waiting for approval

### **Manager Special Powers:**

1. **Assign to Team Member:**
   - Pick specific person from dropdown
   - Task goes directly to them
   
2. **Assign to Team:**
   - Makes task "open" for anyone to pick up
   
3. **Create Tasks:**
   - Non-managers in editorial/design CANNOT create tasks
   - Only managers can

4. **Override Design Return:**
   - Design managers can complete tasks without returning to editorial

---

## 🔄 ALL BUTTON ACTIONS EXPLAINED

### **On Article Detail Page:**

| Button | Who Sees It | What It Does |
|--------|-------------|--------------|
| **Approve Article** | Editorial only, if article is Pending | Opens modal → Can create design task or not |
| **Reject Article** | Editorial only, if article is Pending | Opens modal → Requires rejection reason |
| **Mark as Used** | Editorial only, if article is Approved/Design Ready | Marks article as published in magazine |
| **Edit Article** | CXO Managers only, if article not used | Edit article details |
| **Download File** | Anyone with view access | Downloads attached file |

### **On Task Detail Page:**

| Button | Who Sees It | What It Does |
|--------|-------------|--------------|
| **Pick Up Task** | Your department, if task is Open | Instantly assigns task to you |
| **Mark as Complete** | If task assigned to you | Completes task OR returns to editorial (if design) |
| **Reassign Task** | Managers or dept members | Change assignee or department |
| **Assign to Team (Make Open)** | Managers/dept members, if task is assigned to someone | Unassigns task, makes it open for anyone in dept to pick up |
| **Upload Files** | If task in your dept or assigned to you | Add files to task |

### **On Manager Dashboard:**

| Button | What It Does |
|--------|--------------|
| **Assign to Member** | Quick assign from dashboard |
| **View Details** | Opens full task detail page |
| **Approve/Reject** | For pending CXO articles |

---

## 🚨 COMMON CONFUSIONS EXPLAINED

### **Q: Why didn't the design task get created?**

**A:** The editor UNCHECKED the "Create Design Task" checkbox during approval. Not all articles need design work.

### **Q: Why is the task back in editorial after designer completed it?**

**A:** This is INTENTIONAL! Regular designers must return work to editorial for review. Only design managers can override this.

### **Q: Where did my task go? It's not in my todo list!**

**A:** Check if:
- Task was reassigned to someone else
- Task was completed
- Task was assigned to team (now in "Open Tasks")

### **Q: I can't create a task!**

**A:** Only these roles can create tasks:
- Sales (always)
- CXO (always)
- Editorial **MANAGERS** (not regular editorial)
- Design **MANAGERS** (not regular design)

### **Q: What's the difference between "Approved" and "Design Ready"?**

**A:** 
- **Approved** = Editorial said yes, no design work done yet (or needed)
- **Design Ready** = Design work is completed and ready for publication

### **Q: Can I edit a rejected article?**

**A:** No. Rejected articles are permanent. You'd need to upload a new article.

---

## 🎯 STATUS MEANINGS

### **CXO Article Statuses:**

| Status | What It Means |
|--------|---------------|
| **Pending** | Waiting for editorial to review |
| **Approved** | Editorial approved, no design task created |
| **Rejected** | Editorial rejected (permanent) |
| **Awaiting Design** | Design task created, waiting for designer to pick it up |
| **Designing** | Designer is actively working on it |
| **Design Ready** | Design work complete, ready for publication |
| **Used** | Published in magazine (final state) |

### **Task Statuses:**

| Status | What It Means |
|--------|---------------|
| **Open** | Available for anyone in department to pick up |
| **Assigned** | Assigned to specific person |
| **Review** | Returned from design for editorial review |
| **Completed** | Finished! |

---

## 🔔 NOTIFICATIONS YOU'LL SEE

1. **"New CXO Article uploaded by [user]"** - You have an article to review
2. **"Your article was approved!"** - Your uploaded article got approved
3. **"Your article was rejected. Reason: [reason]"** - Article was rejected
4. **"New design task created"** - Design team has new work
5. **"Task assigned to you"** - You got a new task
6. **"Design work completed"** - Design returned for your review
7. **"Your article marked as used"** - Article is published

---

## 🧪 TESTING GUIDE

### **To Test Complete CXO Workflow:**

1. Login as: **john_sales**
   - Go to "Upload CXO Article"
   - Fill form, upload files
   - Submit

2. Logout, login as: **editorial_manager**
   - See notification
   - Go to "My Todo List"
   - Click article link
   - Click "Approve Article"
   - **CHECK "Create Design Task"**
   - Submit

3. Logout, login as: **designer_sarah**
   - Go to "All Open Tasks"
   - Click "Pick Up Task"
   - Go to "My Todo List"
   - Click task → Upload design files
   - Click "Mark as Complete"
   - See message: "Task returned to editorial"

4. Logout, login as: **editorial_manager**
   - See notification
   - Go to "My Todo List"
   - Review design work
   - Click "Mark as Complete"
   - Go to article detail
   - Click "Mark as Used"

**DONE!** You've completed the full workflow.

---

### **To Test Rejection:**

1. Login as: **ceo_john**
   - Upload article

2. Login as: **editorial_manager**
   - Click "Reject Article"
   - Enter reason: "Missing contact information"
   - Submit

3. Login as: **ceo_john**
   - See rejection notification
   - View article to see rejection reason

---

### **To Test Open Tasks:**

1. Login as: **editorial_manager**
   - Go to Manager Dashboard
   - Find a task
   - Click "Assign to Team"

2. Login as: **editor_jane**
   - Go to "All Open Tasks"
   - Click "Pick Up Task"
   - Task now in your todo list!

---

## 📁 FILE MANAGEMENT

### **Uploading Files:**

- Allowed types: PDF, PNG, JPG, DOC, DOCX, TXT, MP3, WAV, MP4
- Max size: 50 MB
- Files are linked to task history
- Each upload creates a history entry

### **Downloading Files:**

- Click filename to download
- Available to anyone who can view the task/article

### **Deleting Files:**

- Only **Super Admin** can delete
- Files are NOT actually deleted (soft delete)
- `is_deleted` flag is set
- Super Admin can still see deleted files

---

## 🎓 KEY DESIGN DECISIONS

### **Why Auto-Assign to Managers?**

When a task is created for a department, it automatically goes to that department's manager because:
- Managers oversee department workload
- They can then assign to specific team members
- Or assign to team for open pickup

### **Why the Design Return Workflow?**

Design work needs editorial approval because:
- Ensures quality control
- Editorial knows the client requirements
- Catches issues before publication

### **Why Can't Regular Editorial/Design Users Create Tasks?**

To maintain workflow control:
- Managers plan and allocate work
- Prevents task chaos
- Ensures proper task routing

### **Why Sales Can Always Create Tasks?**

Sales brings in client work:
- They initiate the workflow
- They create tasks for other departments
- They upload client articles

---

## 🎬 SUMMARY

**Your app is a magazine production workflow system where:**

1. **Sales/CXO** upload articles from clients
2. **Editorial** reviews and approves/rejects them
3. **Design** creates designs for approved articles
4. **Editorial** reviews design work and marks as used when published

**Key features:**
- ✅ Automatic task routing to department managers
- ✅ Open task pickup system for fair work distribution
- ✅ Design work automatically returns to editorial for review
- ✅ Complete task history and file management
- ✅ Notifications keep everyone informed
- ✅ Manager dashboards for workload monitoring

**Everything is working correctly!** The logic you described is exactly how it's implemented. The confusion was likely because:
- The "Create Design Task" checkbox is optional
- Design completion returns to editorial (by design)
- Status syncing happens automatically in the background

---

**FULL DOCUMENTATION:** See `replit.md` for complete technical details, all button scenarios, edge cases, and troubleshooting guide.
