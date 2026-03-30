from pawpal_system import Owner, Pet, Task, Scheduler

# --- Setup ---
jordan = Owner(name="Jordan")

mochi = Pet(name="Mochi")
luna = Pet(name="Luna")

jordan.add_pet(mochi)
jordan.add_pet(luna)

# --- Tasks for Mochi ---
mochi.add_task(Task(title="Morning walk", duration_minutes=30, priority="high", scheduled_time="07:00", frequency="daily"))
mochi.add_task(Task(title="Evening walk", duration_minutes=20, priority="medium", scheduled_time="18:00", frequency="daily"))
mochi.add_task(Task(title="Flea treatment", duration_minutes=5, priority="low", scheduled_time="09:00", frequency="weekly"))

# --- Tasks for Luna ---
luna.add_task(Task(title="Feeding", duration_minutes=5, priority="high", scheduled_time="08:00", frequency="daily"))
luna.add_task(Task(title="Grooming", duration_minutes=15, priority="low", scheduled_time="14:00", frequency="weekly"))

# --- Build schedule ---
scheduler = Scheduler(owner=jordan)
schedule = scheduler.build_schedule()

# --- Print Today's Schedule ---
print("=" * 40)
print("       Today's Schedule — PawPal+")
print("=" * 40)

if not schedule:
    print("No tasks scheduled for today.")
else:
    for task in schedule:
        time = task.scheduled_time or "  --  "
        status = "✓" if task.completed else "○"
        print(f"  {time}  [{task.priority:<6}]  {status}  {task.title}  ({task.duration_minutes} min)")

print("=" * 40)
