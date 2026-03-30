from pawpal_system import Owner, Pet, Task, Scheduler

# --- Setup ---
jordan = Owner(name="Jordan")

mochi = Pet(name="Mochi")
luna = Pet(name="Luna")

jordan.add_pet(mochi)
jordan.add_pet(luna)

# Tasks added intentionally out of time order to show sorting
mochi.add_task(Task(title="Evening walk", duration_minutes=20, priority="medium", scheduled_time="18:00", frequency="daily"))
mochi.add_task(Task(title="Morning walk", duration_minutes=30, priority="high", scheduled_time="07:00", frequency="daily"))
mochi.add_task(Task(title="Flea treatment", duration_minutes=5, priority="low", scheduled_time="09:00", frequency="weekly"))

luna.add_task(Task(title="Feeding", duration_minutes=5,  priority="high", scheduled_time="08:00", frequency="daily"))
luna.add_task(Task(title="Grooming", duration_minutes=15, priority="low", scheduled_time="14:00", frequency="weekly"))

# Conflict: two tasks at the same time to trigger detection
luna.add_task(Task(title="Vet check", duration_minutes=30, priority="high", scheduled_time="08:00", frequency="once"))

scheduler = Scheduler(owner=jordan)

# --- 1. Sort by time ---
print("=" * 40)
print("  All tasks sorted by time")
print("=" * 40)
all_tasks = jordan.get_all_tasks()
sorted_tasks = scheduler.sort_by_time(all_tasks)
for t in sorted_tasks:
    print(f"  {t.scheduled_time or '--:--'}  {t.title}")

# --- 2. Filter by pet ---
print()
print("=" * 40)
print("  Mochi's tasks only")
print("=" * 40)
for t in scheduler.filter_tasks(pet_name="Mochi"):
    print(f"  {t.title}")

# --- 3. Filter by completion status ---
print()
print("=" * 40)
print("  Incomplete tasks")
print("=" * 40)
for t in scheduler.filter_tasks(completed=False):
    print(f"  {t.title}")

# --- 4. Recurring task: mark complete and verify reschedule ---
print()
print("=" * 40)
print("  Recurring task rescheduling")
print("=" * 40)
walk = mochi.tasks[1]  # Morning walk (daily)
print(f"  Before: '{walk.title}' — completed={walk.completed}, due={walk.due_date}")
scheduler.handle_recurring(walk)
print(f"  After:  '{walk.title}' — completed={walk.completed}, due={walk.due_date}")

# --- 5. Conflict detection ---
print()
print("=" * 40)
print("  Conflict detection")
print("=" * 40)
conflicts = scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(f"  ⚠ {warning}")
else:
    print("  No conflicts.")

# --- 6. Daily schedule (priority + time order) ---
print()
print("=" * 40)
print("       Today's Schedule — PawPal+")
print("=" * 40)
schedule = scheduler.build_schedule()
if not schedule:
    print("  No tasks scheduled for today.")
else:
    for task in schedule:
        time = task.scheduled_time or "  --  "
        status = "✓" if task.completed else "○"
        print(f"  {time}  [{task.priority:<6}]  {status}  {task.title}  ({task.duration_minutes} min)")

print("=" * 40)
