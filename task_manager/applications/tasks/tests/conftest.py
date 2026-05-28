import pytest

from task_manager.applications.labels.models import Label
from task_manager.applications.statuses.models import Status
from task_manager.applications.tasks.models import Task


@pytest.fixture
def create_status(db) -> Status:
    """Создаёт и возвращает статус в базе данных."""
    return Status.objects.create(name="Existing Status")


@pytest.fixture
def create_second_status(db) -> Status:
    """Создаёт и возвращает второй статус в базе данных."""
    return Status.objects.create(name="Second Status")


@pytest.fixture
def create_label(db) -> Label:
    """Создаёт и возвращает метку в базе данных."""
    return Label.objects.create(name="Existing Label")


@pytest.fixture
def create_task(db, create_status, create_user) -> Task:
    """Создаёт и возвращает задачу в базе данных."""
    return Task.objects.create(
        name="Test Task",
        description="Test Description",
        status=create_status,
        author=create_user,
        executor=create_user,
    )
