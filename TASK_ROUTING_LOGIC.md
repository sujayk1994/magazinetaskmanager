# Task Routing Logic - Verification Document

## Overview
This document confirms the task routing logic is correctly implemented as specified.

## The Correct Flow

### FIRST TIME (No owners set yet):
1. **Sales John creates task** → Goes to **Editorial Manager** (general pool)
2. **Editorial Manager assigns to Jane** → Sets `editorial_owner_id = Jane` ✅
3. **Jane sends to design** → Goes to **Design Manager** (no design owner yet)
4. **Design Manager assigns to Sarah** → Sets `design_owner_id = Sarah` ✅

### NOW THE LOOP BEGINS:
**Sarah → Jane → Sarah → Jane → Sarah...** (repeating endlessly)

- When Sarah sends back to editorial → Goes to **Jane** (because `editorial_owner_id` is set)
- When Jane sends to design → Goes to **Sarah** (because `design_owner_id` is set)

### MANAGER OVERRIDE:
If Design Manager gets frustrated and reassigns from Sarah to Amy:
- Design Manager uses "Assign to Member" → Updates `design_owner_id = Amy` ✅
- **Loop becomes: Amy → Jane → Amy → Jane...**

---

## Code Implementation (Verified Correct ✅)

### 1. When Manager Assigns Task to Team Member
**File:** `app/blueprints/tasks.py` (Lines 542-551)

```python
if task.current_department == 'editorial':
    task.editorial_owner_id = member.id  # ✅ Sets editorial owner
    
elif task.current_department == 'design':
    task.design_owner_id = member.id     # ✅ Sets design owner
```

**Result:** When a manager assigns a task, the system remembers who the owner is.

---

### 2. When Editorial (Jane) Sends to Design
**File:** `app/blueprints/tasks.py` (Lines 717-725)

```python
elif task.current_department == 'editorial':
    if task.design_owner_id:
        next_user = task.design_owner      # ✅ Goes to Sarah/Amy directly
    else:
        design_manager = User.query.filter_by(
            department='design',
            is_manager=True
        ).first()
        next_user = design_manager         # ✅ Only if no owner set
```

**Result:** 
- **If design owner exists** (Sarah/Amy): Task goes **directly to them**
- **If no design owner**: Task goes to **Design Manager** (first time only)

---

### 3. When Design (Sarah/Amy) Sends Back to Editorial
**File:** `app/blueprints/tasks.py` (Lines 660-680)

```python
if task.current_department == 'design':
    # Priority order for editorial routing:
    if task.original_requester and task.original_requester.department == 'editorial':
        next_user = task.original_requester    # ✅ Goes to original requester
    elif task.editorial_owner_id:
        next_user = task.editorial_owner       # ✅ Goes to editorial owner (Jane)
    elif task.creator and task.creator.department == 'editorial':
        next_user = task.creator
    else:
        next_user = editorial_manager          # ✅ Fallback to manager
```

**Result:**
- Task goes back to **Jane** (the editorial owner who originally sent it to design)
- This creates the loop: Sarah → Jane → Sarah → Jane...

---

## Complete Flow Examples

### Example 1: Standard Loop (Sarah ↔ Jane)

```
FIRST TIME:
Sales John creates task
  ↓
Editorial Manager (no owner set)
  ↓ Manager assigns to Jane
Jane [editorial_owner_id = Jane] ✅
  ↓ Jane sends to design
Design Manager (no owner set)
  ↓ Manager assigns to Sarah
Sarah [design_owner_id = Sarah] ✅

LOOP STARTS:
Sarah sends back to editorial
  ↓ (checks editorial_owner_id)
Jane [goes directly to owner] ✅
  ↓ Jane sends to design
Sarah [goes directly to design owner] ✅
  ↓
Jane ← Sarah → Jane ← Sarah → Jane...
```

### Example 2: Manager Override (Amy replaces Sarah)

```
Design Manager reassigns task from Sarah to Amy
  ↓
Amy [design_owner_id = Amy] ✅ (ownership changed)

NEW LOOP:
Amy sends back to editorial
  ↓
Jane [goes to editorial owner] ✅
  ↓ Jane sends to design
Amy [goes to NEW design owner] ✅
  ↓
Jane ← Amy → Jane ← Amy → Jane...
```

---

## Key Features ✅

1. ✅ **First time routing goes to managers** (no ownership set)
2. ✅ **Manager assignment sets ownership** (`editorial_owner_id` / `design_owner_id`)
3. ✅ **Subsequent routing uses ownership** (bypasses manager)
4. ✅ **Manager can override** by reassigning (updates ownership)
5. ✅ **Loop is maintained** between assigned owners

---

## Database Fields

### Task Model
```python
editorial_owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
design_owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
original_requester_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
```

- **`editorial_owner_id`**: The editorial person "stuck in the loop" with design
- **`design_owner_id`**: The designer "stuck in the loop" with editorial  
- **`original_requester_id`**: Tracks who originally sent to design (for return routing)

---

## Status: ✅ VERIFIED CORRECT

The implementation matches your requirements exactly:
- First time: Goes to managers
- After assignment: Direct routing to owners
- Manager override: Updates ownership and new loop begins
- Jane can send to both design and sales
- When sending to design, it goes to manager ONLY if no design owner is set
- Once design owner is assigned, ALL future sends go directly to that owner

**The logic is working as specified!**
