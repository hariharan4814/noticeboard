from django.db import models
from django.conf import settings


class Notice(models.Model):
    NOTICE_TYPES = [
        ("General", "General"),
        ("Exam", "Exam"),
        ("Event", "Event"),
        ("Placement", "Placement"),
        ("Holiday", "Holiday"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    notice_type = models.CharField(
        max_length=20,
        choices=NOTICE_TYPES,
        default="General"
    )

    attachment = models.FileField(
        upload_to="notices/",
        blank=True,
        null=True
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title