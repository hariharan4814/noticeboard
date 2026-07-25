from django import forms
from .models import Notice


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = [
            "title",
            "description",
            "notice_type",
            "attachment",
            "is_active",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                }
            ),
            "notice_type": forms.Select(
                attrs={"class": "form-select"}
            ),
            "attachment": forms.FileInput(
                attrs={"class": "form-control"}
            ),
            "is_active": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }