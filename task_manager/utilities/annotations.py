from __future__ import annotations

from typing import TYPE_CHECKING

from django.db.models import Value
from django.db.models.functions import Concat

if TYPE_CHECKING:
    from django.db.models.expressions import Expression


def get_user_full_name_annotation() -> dict[str, Expression]:
    return {"full_name": Concat("first_name", Value(" "), "last_name")}
