from django import forms
from .models import Student


class StudentForm(forms.ModelForm):
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