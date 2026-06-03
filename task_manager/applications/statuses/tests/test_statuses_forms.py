"""
Тесты для форм приложения statuses.

Модуль task_manager.applications.statuses.forms содержит:
- StatusCreateForm — форма создания статуса
- StatusUpdateForm — форма обновления статуса
"""

from task_manager.applications.statuses.forms import StatusCreateForm, StatusUpdateForm
from task_manager.applications.statuses.models import Status


class TestStatusCreateForm:
    """Тесты для StatusCreateForm."""

    def test_valid_form_creates_status(self, db):
        """Валидная форма создаёт статус."""
        form = StatusCreateForm(data={"name": "in_progress"})
        assert form.is_valid()
        status = form.save()
        assert status.name == "in_progress"

    def test_invalid_form_missing_name(self):
        """Форма без имени невалидна."""
        form = StatusCreateForm(data={})
        assert not form.is_valid()
        assert "name" in form.errors

    def test_form_has_name_field(self):
        """Форма содержит поле name."""
        form = StatusCreateForm()
        assert "name" in form.fields

    def test_form_meta_model(self):
        """Форма связана с моделью Status."""
        assert StatusCreateForm._meta.model is Status


class TestStatusUpdateForm:
    """Тесты для StatusUpdateForm."""

    def test_valid_form_updates_status(self, db):
        """Валидная форма обновляет статус."""
        status = Status.objects.create(name="in_progress")
        form = StatusUpdateForm(data={"name": "done"}, instance=status)
        assert form.is_valid()
        updated_status = form.save()
        assert updated_status.name == "done"

    def test_invalid_form_missing_name(self):
        """Форма без имени невалидна."""
        form = StatusUpdateForm(data={})
        assert not form.is_valid()
        assert "name" in form.errors

    def test_form_has_name_field(self):
        """Форма содержит поле name."""
        form = StatusUpdateForm()
        assert "name" in form.fields

    def test_form_meta_model(self):
        """Форма связана с моделью Status."""
        assert StatusUpdateForm._meta.model is Status
