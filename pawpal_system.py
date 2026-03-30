from dataclasses import dataclass, field
from datetime import date
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
        pass


@dataclass
class Pet:
    name: str
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to this pet's task list."""
        pass

    def remove_task(self, task: Task):
        """Remove a task from this pet's task list if it exists."""
        pass

    def get_tasks(self) -> list:
        """Return all tasks for this pet."""
        pass


@dataclass
class Owner:
    name: str
    pets: list = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Add a pet to this owner's list."""
        pass

    def remove_pet(self, pet: Pet):
        """Remove a pet from this owner's list if it exists."""
        pass

    def get_all_tasks(self) -> list:
        """Return every task across all pets."""
        pass


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def build_schedule(self) -> list:
        """Build an ordered daily plan from all tasks, respecting priority and time."""
        pass

    def sort_by_time(self, tasks: list) -> list:
        """Return tasks sorted by scheduled_time (HH:MM)."""
        pass

    def filter_tasks(self, pet_name: Optional[str] = None, completed: Optional[bool] = None) -> list:
        """Return tasks filtered by pet name and/or completion status."""
        pass

    def detect_conflicts(self) -> list:
        """Return a list of warning messages for tasks scheduled at the same time."""
        pass

    def handle_recurring(self, task: Task):
        """After a recurring task is completed, create the next occurrence."""
        pass
