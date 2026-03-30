import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+. This UI calls into your PawPal+ scheduling logic in `pawpal_system.py`.

Add tasks, generate a schedule, and use the same sorting/filtering/conflict ideas you implemented in Python.
"""
)

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

# Initialize Owner and Pet in session state so data persists across rerenders
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name)
    st.session_state.owner.add_pet(Pet(name=pet_name))
else:
    st.session_state.owner.name = owner_name
    if st.session_state.owner.pets:
        st.session_state.owner.pets[0].name = pet_name

pet: Pet = st.session_state.owner.pets[0]

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

# Optional details used for sorting + conflict warnings
col4, col5 = st.columns(2)
with col4:
    scheduled_time = st.text_input("Time (HH:MM, optional)", value="")
with col5:
    frequency = st.selectbox("Frequency", ["once", "daily", "weekly"], index=0)

if st.button("Add task"):
    pet.add_task(
        Task(
            title=task_title,
            duration_minutes=int(duration),
            priority=priority,
            scheduled_time=scheduled_time.strip() or None,
            frequency=frequency,
        )
    )

tasks = pet.get_tasks()
if tasks:
    st.write("Current tasks:")
    for i, t in enumerate(tasks):
        status = "Done" if t.completed else "To do"
        due = t.due_date.isoformat() if t.due_date else ""
        time = t.scheduled_time or "—"

        c1, c2, c3, c4, c5 = st.columns([3, 2, 2, 2, 2])
        with c1:
            st.write(f"**{t.title}** ({status})")
        with c2:
            st.write(f"Priority: {t.priority}")
        with c3:
            st.write(f"Time: {time}")
        with c4:
            st.write(f"Freq: {t.frequency}")
            if due:
                st.write(f"Due: {due}")
        with c5:
            if not t.completed and st.button("Mark complete", key=f"complete_{i}"):
                t.mark_complete()
                st.success(f"Marked '{t.title}' complete.")
                st.rerun()
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner=st.session_state.owner)
    pet_name = pet.name

    incomplete_tasks = scheduler.filter_tasks(pet_name=pet_name, completed=False)

    # Conflicts: lightweight exact-time check on the same set the schedule uses
    warnings = []
    seen = {}
    for task in incomplete_tasks:
        if task.scheduled_time is None:
            continue
        if task.scheduled_time in seen:
            warnings.append(
                f"Conflict at {task.scheduled_time}: '{task.title}' overlaps with '{seen[task.scheduled_time]}'"
            )
        else:
            seen[task.scheduled_time] = task.title

    for warning in warnings:
        st.warning(warning)

    # Priority schedule (incomplete only) + chronological view (can include completed)
    priority_schedule = scheduler.build_schedule()
    chron_view = scheduler.sort_by_time(incomplete_tasks)

    if not priority_schedule:
        st.info("Nothing to schedule (no incomplete tasks).")
    else:
        st.success(f"Scheduled {len(priority_schedule)} task(s) for today.")
        st.caption("Priority schedule = priority (high→low) then time.")
        st.table(
            [
                {
                    "Time": t.scheduled_time or "—",
                    "Task": t.title,
                    "Priority": t.priority,
                    "Duration (min)": t.duration_minutes,
                    "Frequency": t.frequency,
                    "Due date": t.due_date.isoformat() if t.due_date else "—",
                }
                for t in priority_schedule
            ]
        )

    if chron_view:
        st.subheader("Chronological (by time)")
        st.table(
            [
                {
                    "Time": t.scheduled_time or "—",
                    "Task": t.title,
                    "Priority": t.priority,
                    "Frequency": t.frequency,
                }
                for t in chron_view
            ]
        )
