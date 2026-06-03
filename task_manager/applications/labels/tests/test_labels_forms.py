"""
Тесты для форм приложения labels.

Модуль task_manager.applications.labels.forms содержит:
- LabelCreateForm — форма создания метки
- LabelUpdateForm — форма обновления метки
"""

from __future__ import annotations

from task_manager.applications.labels.forms import LabelCreateForm, LabelUpdateForm
from task_manager.applications.labels.models import Label


class TestLabelCreateForm:
    """Тесты для LabelCreateForm."""

    def test_valid_form_creates_label(self, db):
        """Валидная форма создаёт метку."""
        form = LabelCreateForm(data={"name": "bug"})
        assert form.is_valid()
        label = form.save()
        assert label.name == "bug"

    def test_invalid_form_missing_name(self):
        """Форма без имени невалидна."""
        form = LabelCreateForm(data={})
        assert not form.is_valid()
        assert "name" in form.errors

    def test_form_has_name_field(self):
        """Форма содержит поле name."""
        form = LabelCreateForm()
        assert "name" in form.fields

    def test_form_meta_model(self):
        """Форма связана с моделью Label."""
        assert LabelCreateForm._meta.model is Label


class TestLabelUpdateForm:
    """Тесты для LabelUpdateForm."""

    def test_valid_form_updates_label(self, db):
        """Валидная форма обновляет метку."""
        label = Label.objects.create(name="bug")
        form = LabelUpdateForm(data={"name": "feature"}, instance=label)
        assert form.is_valid()
        updated_label = form.save()
        assert updated_label.name == "feature"

    def test_invalid_form_missing_name(self):
        """Форма без имени невалидна."""
        form = LabelUpdateForm(data={})
        assert not form.is_valid()
        assert "name" in form.errors

    def test_form_has_name_field(self):
        """Форма содержит поле name."""
        form = LabelUpdateForm()
        assert "name" in form.fields

    def test_form_meta_model(self):
        """Форма связана с моделью Label."""
        assert LabelUpdateForm._meta.model is Label
