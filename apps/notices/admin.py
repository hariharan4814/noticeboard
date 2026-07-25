from django.contrib import admin
from .models import Notice


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "notice_type",
        "created_by",
        "created_at",
        "is_active",
    )

    list_filter = (
        "notice_type",
        "is_active",
    )

    search_fields = (
        "title",
        "description",
    )