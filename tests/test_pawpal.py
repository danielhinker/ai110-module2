"""Tests for core Task/Pet behavior and Scheduler algorithms."""

from datetime import date, timedelta

import pytest

from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_changes_status():
    """One-off task: mark_complete sets completed to True."""
    task = Task(title="Bath time", duration_minutes=20, priority="medium")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    """Adding a task to a Pet increases its task list."""
    pet = Pet(name="Mochi")
    assert len(pet.tasks) == 0
    pet.add_task(Task(title="Walk", duration_minutes=30, priority="high"))
    assert len(pet.tasks) == 1


def test_sort_by_time_chronological():
    """Tasks are returned in chronological order by scheduled_time (HH:MM)."""
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi")
    owner.add_pet(pet)
    pet.add_task(Task(title="Evening", duration_minutes=20, priority="medium", scheduled_time="18:00"))
    pet.add_task(Task(title="Morning", duration_minutes=30, priority="high", scheduled_time="07:00"))
    pet.add_task(Task(title="Noon", duration_minutes=10, priority="low", scheduled_time="12:00"))

    scheduler = Scheduler(owner=owner)
    ordered = scheduler.sort_by_time(owner.get_all_tasks())
    assert [t.scheduled_time for t in ordered] == ["07:00", "12:00", "18:00"]


def test_daily_recurrence_advances_due_date():
    """Daily task: after mark_complete, due_date is tomorrow and task stays incomplete for the next cycle."""
    task = Task(title="Meds", duration_minutes=5, priority="high", frequency="daily")
    task.mark_complete()
    assert task.completed is False
    assert task.due_date == date.today() + timedelta(days=1)


def test_conflict_detection_flags_duplicate_time():
    """Two tasks at the same scheduled time produce a warning."""
    owner = Owner(name="Jordan")
    pet = Pet(name="Luna")
    owner.add_pet(pet)
    pet.add_task(Task(title="Feeding", duration_minutes=5, priority="high", scheduled_time="08:00"))
    pet.add_task(Task(title="Vet check", duration_minutes=30, priority="high", scheduled_time="08:00"))

    scheduler = Scheduler(owner=owner)
    warnings = scheduler.detect_conflicts()
    assert len(warnings) == 1
    assert "08:00" in warnings[0]
    assert "Feeding" in warnings[0] or "Vet" in warnings[0]


def test_build_schedule_empty_when_no_tasks():
    """Owner with a pet but no tasks yields an empty schedule."""
    owner = Owner(name="Jordan")
    owner.add_pet(Pet(name="Solo"))
    scheduler = Scheduler(owner=owner)
    assert scheduler.build_schedule() == []
