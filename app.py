import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
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

if st.button("Add task"):
    pet.add_task(Task(
        title=task_title,
        duration_minutes=int(duration),
        priority=priority,
    ))

if pet.get_tasks():
    st.write("Current tasks:")
    st.table([
        {"title": t.title, "duration_minutes": t.duration_minutes, "priority": t.priority}
        for t in pet.get_tasks()
    ])
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner=st.session_state.owner)
    schedule = scheduler.build_schedule()
    conflicts = scheduler.detect_conflicts()

    for warning in conflicts:
        st.warning(warning)

    if not schedule:
        st.info("No tasks to schedule.")
    else:
        st.success(f"Scheduled {len(schedule)} task(s) for today.")
        st.table([
            {
                "Time": t.scheduled_time or "—",
                "Task": t.title,
                "Priority": t.priority,
                "Duration (min)": t.duration_minutes,
            }
            for t in schedule
        ])
