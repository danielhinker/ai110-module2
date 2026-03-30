import pytest
from pawpal_system import Task, Pet


def test_mark_complete_changes_status():
    """Task.mark_complete() should set completed to True for a one-time task."""
    task = Task(title="Bath time", duration_minutes=20, priority="medium")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    """Adding a task to a Pet should increase its task list by one."""
    pet = Pet(name="Mochi")
    assert len(pet.tasks) == 0
    pet.add_task(Task(title="Walk", duration_minutes=30, priority="high"))
    assert len(pet.tasks) == 1
