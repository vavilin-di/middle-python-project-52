__all__ = ["TaskCreateView", "TaskDeleteView", "TaskDetailView", "TaskListView", "TaskUpdateView"]

from .create import TaskCreateView
from .delete import TaskDeleteView
from .list import TaskDetailView, TaskListView
from .update import TaskUpdateView
