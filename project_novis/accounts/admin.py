from django import forms
from django.contrib import admin
from django.contrib.auth import password_validation
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from django.utils.translation import gettext_lazy as _
from .models import User, UserValidation


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ('email', 'is_staff', 'is_active', 'name',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(BaseUserChangeForm):
    """
    Override as needed
    """


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'name', 'is_staff', 'validated')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('name', 'email')

    readonly_fields = ('created', 'modified', 'validated')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('name', 'validated')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'created', 'modified')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )
    ordering = ('email',)


@admin.register(UserValidation)
class UserValidationAdmin(admin.ModelAdmin):
    list_display = ("user", "approved")
    list_display_links = ("user",)
    list_filter = ("approved", "approved_at", "approved_by")

    fieldsets = (
        (_('Submitted data'), {'fields': ('user', 'validation_comment', 'validation_file')}),
        (_('Approves'), {'fields': ('approved', 'approved_at', 'approved_by')}),
        (_('Advanced options'), {'fields': ('created', 'modified')}),
    )

    readonly_fields = ('created', 'modified')
    raw_id_fields = ("user", "approved_by")
