from django import forms
from django.contrib import admin

from .models import User

# Register your models here.


class UserForm(forms.ModelForm):
    new_password = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter new password to change, leave blank to keep current"
            }
        ),
        required=False,
    )

    class Meta:
        model = User
        fields = "__all__"
        exclude = ("password",)  # Exclude the original password field

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get("new_password")

        if new_password:  # Only set a new password if one was provided
            user.set_password(new_password)

        if commit:
            user.save()

        return user


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserForm
    list_display = ("id", "username")
    list_filter = ()
    search_fields = ("username",)
