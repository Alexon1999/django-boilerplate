from django import forms
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import Departement, Service, Unite, User


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

        update_fields = []

        if self.initial.get("unite"):
            if self.initial["unite"] != self.cleaned_data["unite"]:
                update_fields.append("unite")

        if new_password:  # Only set a new password if one was provided
            user.set_password(new_password)

        if commit:
            user.save()

        if len(update_fields) > 0:
            user.save(update_fields=update_fields)

        return user


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserForm
    list_display = ("id", "username")
    list_filter = ()
    search_fields = ("username",)


admin.site.register(Departement, SimpleHistoryAdmin)
admin.site.register(Service)
admin.site.register(Unite)
