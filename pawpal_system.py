from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str  # "low", "medium", "high"
    scheduled_time: Optional[str] = None  # "HH:MM" format
    frequency: str = "once"  # "once", "daily", "weekly"
    completed: bool = False

    def mark_complete(self):
        """Mark this task as done and set a new due date if it recurs."""
        self.completed = True


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
