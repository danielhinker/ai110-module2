from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Optional


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str  # "low", "medium", "high"
    scheduled_time: Optional[str] = None  # "HH:MM" format
    frequency: str = "once"  # "once", "daily", "weekly"
    completed: bool = False
    due_date: Optional[date] = None

    def mark_complete(self):
        """Mark this task as done and set a new due date if it recurs."""
        self.completed = True
        if self.frequency == "daily":
            self.due_date = date.today() + timedelta(days=1)
            self.completed = False
        elif self.frequency == "weekly":
            self.due_date = date.today() + timedelta(weeks=1)
            self.completed = False


@dataclass
class Pet:
    name: str
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task: Task):
        """Remove a task from this pet's task list if it exists."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks(self) -> list:
        """Return all tasks for this pet."""
        return self.tasks


@dataclass
class Owner:
    name: str
    pets: list = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Add a pet to this owner's list."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet):
        """Remove a pet from this owner's list if it exists."""
        if pet in self.pets:
            self.pets.remove(pet)

    def get_all_tasks(self) -> list:
        """Return every task across all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

    def __init__(self, owner: Owner):
        self.owner = owner

    def build_schedule(self) -> list:
        """Build an ordered daily plan from all tasks, respecting priority and time."""
        tasks = self.owner.get_all_tasks()
        incomplete = [t for t in tasks if not t.completed]
        return sorted(
            incomplete,
            key=lambda t: (
                self.PRIORITY_ORDER.get(t.priority, 99),
                t.scheduled_time or "99:99",
            ),
        )

    def sort_by_time(self, tasks: list) -> list:
        """Return tasks sorted by scheduled_time (HH:MM)."""
        return sorted(tasks, key=lambda t: t.scheduled_time or "99:99")

    def filter_tasks(self, pet_name: Optional[str] = None, completed: Optional[bool] = None) -> list:
        """Return tasks filtered by pet name and/or completion status."""
        results = []
        for pet in self.owner.pets:
            if pet_name and pet.name.lower() != pet_name.lower():
                continue
            for task in pet.get_tasks():
                if completed is not None and task.completed != completed:
                    continue
                results.append(task)
        return results

    def detect_conflicts(self) -> list:
        """Return a list of warning messages for tasks scheduled at the same time."""
        seen = {}
        warnings = []
        for pet in self.owner.pets:
            for task in pet.get_tasks():
                if task.scheduled_time is None:
                    continue
                if task.scheduled_time in seen:
                    warnings.append(
                        f"Conflict at {task.scheduled_time}: '{task.title}' overlaps with '{seen[task.scheduled_time]}'"
                    )
                else:
                    seen[task.scheduled_time] = task.title
        return warnings

    def handle_recurring(self, task: Task):
        """After a recurring task is completed, create the next occurrence."""
        task.mark_complete()
