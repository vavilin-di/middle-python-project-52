from django.contrib.postgres.aggregates import ArrayAgg
from django.db import connection
from django.db.models import Aggregate, JSONField

match connection.vendor:
    case "postgresql":
        ArrayAggregation = ArrayAgg
    case "sqlite":

        class ArrayAggregation(Aggregate):
            function = "JSON_GROUP_ARRAY"
            output_field = JSONField()
            template = "%(function)s(%(distinct)s%(expressions)s)"

    case _:
        raise AssertionError(f"Unsupported database vendor {connection.vendor}")
