__all__ = ["ArrayAggregation", "get_array_aggregation"]

from typing import Self

from django.contrib.postgres.aggregates import ArrayAgg
from django.db import connection
from django.db.models import Aggregate, JSONField, Value


class SQLiteArrayAggregation(Aggregate):
    """Аналог агрегатной функции ArrayAgg для SQLite"""

    function = "JSON_GROUP_ARRAY"
    output_field = JSONField()
    template = "%(function)s(%(distinct)s%(expressions)s)"

    def resolve_expression(self, query, allow_joins=True, reuse=None, summarize=False, for_save=False) -> Self:  # type: ignore[override]
        if self.default is not None and isinstance(self.default, Value):  # type: ignore[has-type]``
            self.default = Value("[]", output_field=JSONField())
        return super().resolve_expression(query, allow_joins, reuse, summarize, for_save)


def get_array_aggregation() -> type[ArrayAgg] | type[SQLiteArrayAggregation]:
    """Возвращает класс агрегатной функции в зависимости от БД.

    Returns:
        ArrayAgg для PostgreSQL, SQLiteArrayAggregation для SQLite.

    Raises:
        AssertionError: если БД не поддерживается.
    """
    match connection.vendor:
        case "postgresql":
            return ArrayAgg
        case "sqlite":
            return SQLiteArrayAggregation
        case _:
            msg = f"Неподдерживаемый вендор базы данных: {connection.vendor}"
            raise AssertionError(msg)


ArrayAggregation: type[ArrayAgg] | type[SQLiteArrayAggregation] = get_array_aggregation()
