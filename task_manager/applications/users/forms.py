from django.contrib.auth.forms import UserCreationForm


class CustomUserCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ("first_name", "last_name", *UserCreationForm.Meta.fields)


class CustomUserUpdateForm(CustomUserCreateForm):
    def clean_username(self):
        return self.cleaned_data.get("username")
