"""
Тесты для модуля aggregates.py.

Модуль task_manager.utilities.aggregates определяет агрегатную функцию
ArrayAggregation, которая работает как с PostgreSQL (через ArrayAgg),
так и с SQLite (через кастомный Aggregate с JSON_GROUP_ARRAY).

Код выполняется на уровне импорта модуля, поэтому для тестирования
разных веток используется перезагрузка модуля с подменой connection.vendor.
"""

import importlib
from unittest.mock import patch

import pytest
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Aggregate, JSONField


class TestArrayAggregationSQLite:
    """Тесты для ветки SQLite (используется в тестовом окружении по умолчанию)."""

    def test_is_aggregate_subclass(self):
        """ArrayAggregation должен быть подклассом Aggregate в режиме SQLite."""
        import task_manager.utilities.aggregates as agg

        assert issubclass(agg.ArrayAggregation, Aggregate)

    def test_is_not_arrayagg(self):
        """ArrayAggregation НЕ должен быть ArrayAgg в режиме SQLite."""
        import task_manager.utilities.aggregates as agg

        assert agg.ArrayAggregation is not ArrayAgg

    def test_has_correct_function(self):
        """Проверка SQL-функции JSON_GROUP_ARRAY."""
        import task_manager.utilities.aggregates as agg

        assert agg.ArrayAggregation.function == "JSON_GROUP_ARRAY"

    def test_has_jsonfield_output(self):
        """Проверка, что output_field — это JSONField."""
        import task_manager.utilities.aggregates as agg

        assert isinstance(agg.ArrayAggregation.output_field, JSONField)

    def test_has_correct_template(self):
        """Проверка SQL-шаблона."""
        import task_manager.utilities.aggregates as agg

        expected_template = "%(function)s(%(distinct)s%(expressions)s)"
        assert agg.ArrayAggregation.template == expected_template

    def test_can_be_used_in_annotation(self, db):
        """ArrayAggregation должен работать в annotate() на SQLite.

        Интеграционный тест: создаём модель с M2M и проверяем,
        что агрегация возвращает корректный JSON-массив.
        """
        from django.contrib.auth.models import User

        from task_manager.applications.labels.models import Label
        from task_manager.applications.statuses.models import Status
        from task_manager.applications.tasks.models import Task
        from task_manager.utilities.aggregates import ArrayAggregation

        status = Status.objects.create(name="Status")
        author = User.objects.create_user(username="author", password="pass123")
        executor = User.objects.create_user(username="executor", password="pass123")

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
            .annotate(label_names=ArrayAggregation("labels__name"))
            .values("id", "label_names")
            .first()
        )

        assert result is not None
        # SQLite возвращает JSON-строку, а не список
        label_names = result["label_names"]
        assert label_names is not None
        assert "Bug" in str(label_names)
        assert "Feature" in str(label_names)


class TestArrayAggregationPostgreSQL:
    """Тесты для ветки PostgreSQL.

    В тестовом окружении используется SQLite, поэтому для проверки
    PostgreSQL-ветки мокаем connection.vendor.
    """

    def test_is_arrayagg_when_postgresql(self):
        """При vendor='postgresql' ArrayAggregation должен быть ArrayAgg."""
        with patch("django.db.connection.vendor", "postgresql"):
            import importlib

            import task_manager.utilities.aggregates as agg

            importlib.reload(agg)

            assert agg.ArrayAggregation is ArrayAgg

    def test_is_aggregate_subclass_when_postgresql(self):
        """При vendor='postgresql' ArrayAggregation должен быть подклассом Aggregate."""
        with patch("django.db.connection.vendor", "postgresql"):
            import task_manager.utilities.aggregates as agg

            importlib.reload(agg)

            assert issubclass(agg.ArrayAggregation, Aggregate)

    def test_raises_on_unsupported_vendor(self):
        """При неподдерживаемом vendor должно подниматься AssertionError."""
        with (
            patch("django.db.connection.vendor", "mysql"),
            pytest.raises(AssertionError, match="Unsupported database vendor mysql"),
        ):
            import task_manager.utilities.aggregates as agg

            importlib.reload(agg)

    def test_raises_on_oracle(self):
        """Проверка ещё одного неподдерживаемого vendor."""
        with (
            patch("django.db.connection.vendor", "oracle"),
            pytest.raises(AssertionError, match="Unsupported database vendor oracle"),
        ):
            import task_manager.utilities.aggregates as agg

            importlib.reload(agg)
