__all__ = ["ArrayAggregation"]

from django.contrib.postgres.aggregates import ArrayAgg
from django.db import connection
from django.db.models import Aggregate, JSONField, Value

match connection.vendor:
    case "postgresql":
        ArrayAggregation = ArrayAgg
    case "sqlite":

        class ArrayAggregation(Aggregate):
            function = "JSON_GROUP_ARRAY"
            output_field = JSONField()
            template = "%(function)s(%(distinct)s%(expressions)s)"

            def resolve_expression(self, query, allow_joins=True, reuse=None, summarize=False, for_save=False):
                if self.default is not None and isinstance(self.default, Value):
                    self.default = Value("[]", output_field=JSONField())
                return super().resolve_expression(query, allow_joins, reuse, summarize, for_save)

    case _:
        raise AssertionError(f"Unsupported database vendor {connection.vendor}")
