"""
Тесты для модуля aggregates.py.

Модуль task_manager.utilities.aggregates определяет агрегатную функцию
ArrayAggregation, которая работает как с PostgreSQL (через ArrayAgg),
так и с SQLite (через кастомный SQLiteArrayAggregation с JSON_GROUP_ARRAY).

Вместо перезагрузки модуля через importlib.reload() тесты напрямую
тестируют функцию get_array_aggregation() с подменой connection.vendor.
"""

from unittest.mock import patch

import pytest
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Aggregate, JSONField

from task_manager.utilities.aggregates import SQLiteArrayAggregation, get_array_aggregation


class TestGetArrayAggregationFunction:
    """Тесты для функции get_array_aggregation()."""

    def test_returns_sqlite_array_aggregation_when_sqlite(self):
        """При vendor='sqlite' должна возвращаться SQLiteArrayAggregation."""
        with patch("django.db.connection.vendor", "sqlite"):
            result = get_array_aggregation()
        assert result is SQLiteArrayAggregation

    def test_returns_arrayagg_when_postgresql(self):
        """При vendor='postgresql' должна возвращаться ArrayAgg."""
        with patch("django.db.connection.vendor", "postgresql"):
            result = get_array_aggregation()
        assert result is ArrayAgg

    def test_raises_on_unsupported_vendor(self):
        """При неподдерживаемом vendor должно подниматься AssertionError."""
        with (
            patch("django.db.connection.vendor", "mysql"),
            pytest.raises(AssertionError, match="Неподдерживаемый вендор базы данных: mysql"),
        ):
            get_array_aggregation()


class TestSQLiteArrayAggregationClass:
    """Тесты для класса SQLiteArrayAggregation."""

    def test_is_aggregate_subclass(self):
        """SQLiteArrayAggregation должен быть подклассом Aggregate."""
        assert issubclass(SQLiteArrayAggregation, Aggregate)

    def test_is_not_arrayagg(self):
        """SQLiteArrayAggregation НЕ должен быть ArrayAgg."""
        assert SQLiteArrayAggregation is not ArrayAgg

    def test_has_correct_function(self):
        """Проверка SQL-функции JSON_GROUP_ARRAY."""
        assert SQLiteArrayAggregation.function == "JSON_GROUP_ARRAY"

    def test_has_jsonfield_output(self):
        """Проверка, что output_field — это JSONField."""
        assert isinstance(SQLiteArrayAggregation.output_field, JSONField)

    def test_has_correct_template(self):
        """Проверка SQL-шаблона."""
        expected_template = "%(function)s(%(distinct)s%(expressions)s)"
        assert SQLiteArrayAggregation.template == expected_template

    def test_can_be_used_in_annotation(self, db, existing_password: str):
        """SQLiteArrayAggregation должен работать в annotate() на SQLite.

        Интеграционный тест: создаём модель с M2M и проверяем,
        что агрегация возвращает корректный JSON-массив.
        """
        from django.contrib.auth.models import User

        from task_manager.applications.labels.models import Label
        from task_manager.applications.statuses.models import Status
        from task_manager.applications.tasks.models import Task

        status = Status.objects.create(name="Status")
        author = User.objects.create_user(username="author", password=existing_password)
        executor = User.objects.create_user(username="executor", password=existing_password)

        label1 = Label.objects.create(name="Bug")
        label2 = Label.objects.create(name="Feature")

        task = Task.objects.create(
            name="Test Task",
            description="Test",
            status=status,
            author=author,
            executor=executor,
        )
        task.labels.add(label1, label2)

        result = (
            Task.objects.filter(pk=task.pk)
            .annotate(label_names=SQLiteArrayAggregation("labels__name"))
            .values("id", "label_names")
            .first()
        )

        assert result is not None
        # SQLite возвращает JSON-строку, а не список
        label_names = result["label_names"]
        assert label_names is not None
        assert "Bug" in str(label_names)
        assert "Feature" in str(label_names)


class TestArrayAggregationModuleLevel:
    """Тесты для модульного уровня ArrayAggregation.

    Проверяем, что ArrayAggregation (результат вызова get_array_aggregation()
    на уровне модуля) корректен для текущего окружения (SQLite).
    """

    def test_array_aggregation_is_sqlite_array_aggregation(self):
        """В тестовом окружении (SQLite) ArrayAggregation должен быть SQLiteArrayAggregation."""
        from task_manager.utilities.aggregates import ArrayAggregation

        assert ArrayAggregation is SQLiteArrayAggregation

    def test_array_aggregation_is_aggregate_subclass(self):
        """ArrayAggregation должен быть подклассом Aggregate."""
        from task_manager.utilities.aggregates import ArrayAggregation

        assert issubclass(ArrayAggregation, Aggregate)
