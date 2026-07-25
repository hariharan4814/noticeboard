from django.db import models


class Student(models.Model):

    YEAR_CHOICES = [
        ("1", "First Year"),
        ("2", "Second Year"),
        ("3", "Third Year"),
        ("4", "Fourth Year"),
    ]

    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    year = models.CharField(max_length=1, choices=YEAR_CHOICES)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.roll_number} - {self.name}"