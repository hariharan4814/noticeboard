from django import forms
from django.db import transaction
from .models import Student


class StudentForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        help_text="Required for new students."
    )
    password = forms.CharField(
        max_length=128,
        required=False,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        help_text="Required for new students. Leave blank on update unless changing password."
    )

    class Meta:
        model = Student
        fields = [
            "name",
            "roll_number",
            "department",
            "year",
            "email",
            "phone",
        ]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "roll_number": forms.TextInput(attrs={"class": "form-control"}),
            "department": forms.TextInput(attrs={"class": "form-control"}),
            "year": forms.Select(attrs={"class": "form-select"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If editing an existing student, pre-populate the username
        if self.instance and self.instance.pk and self.instance.user:
            self.fields["username"].initial = self.instance.user.username
            self.fields["username"].help_text = "Leave as is or update the login username."
            self.fields["password"].help_text = "Leave blank unless you want to change the password."
        else:
            self.fields["username"].required = True
            self.fields["password"].required = True

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if username:
            from apps.accounts.models import CustomUser
            qs = CustomUser.objects.filter(username=username)
            if self.instance and self.instance.pk and self.instance.user:
                qs = qs.exclude(pk=self.instance.user.pk)
            if qs.exists():
                raise forms.ValidationError("A user with that username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email:
            from apps.accounts.models import CustomUser
            qs_user = CustomUser.objects.filter(email=email)
            if self.instance and self.instance.pk and self.instance.user:
                qs_user = qs_user.exclude(pk=self.instance.user.pk)
            if qs_user.exists():
                raise forms.ValidationError("A user with that email address already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        # Validation for new student
        if not self.instance.pk:
            if not username:
                self.add_error("username", "Username is required for new students.")
            if not password:
                self.add_error("password", "Password is required for new students.")
        else:
            # If editing and admin starts setting up a user account for a student that didn't have one
            if username and not self.instance.user:
                if not password:
                    self.add_error("password", "Password is required when creating a new user account.")
        return cleaned_data

    @transaction.atomic
    def save(self, commit=True):
        from apps.accounts.models import CustomUser

        student = super().save(commit=False)
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        email = self.cleaned_data.get("email")

        if student.pk and student.user:
            # Update existing CustomUser
            user = student.user
            if username:
                user.username = username
            if email:
                user.email = email
            if password:
                user.set_password(password)
            user.save()
        else:
            # Create new CustomUser
            if username:
                user = CustomUser.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    role=CustomUser.Role.STUDENT
                )
                student.user = user

        if commit:
            student.save()
        return student