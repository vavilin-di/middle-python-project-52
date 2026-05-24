from django.contrib.auth.forms import UserCreationForm


class CustomUserCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ("first_name", "last_name", *UserCreationForm.Meta.fields)


class CustomUserUpdateForm(CustomUserCreateForm):
    def clean_username(self):
        """Reject usernames that differ only in case."""
        return self.cleaned_data.get("username")
