from django.db.models import Value
from django.db.models.expressions import Expression
from django.db.models.functions import Concat


def get_user_full_name_annotation() -> dict[str, Expression]:
    return {"full_name": Concat("first_name", Value(" "), "last_name")}
