__all__ = ["StatusCreateForm", "StatusUpdateForm"]

from django.forms import ModelForm

from .models import Status


class StatusCreateForm(ModelForm):
    class Meta:
        model = Status
        fields = ("name",)


class StatusUpdateForm(ModelForm):
    class Meta:
        model = Status
        fields = ("name",)
