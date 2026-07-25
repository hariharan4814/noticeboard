from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Student


@login_required
def student_list(request):
    students = Student.objects.all().order_by("roll_number")

    return render(
        request,
        "students/student_list.html",
        {"students": students},
    )


@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)

    return render(
        request,
        "students/student_detail.html",
        {"student": student},
    )


@login_required
def student_create(request):
    return render(request, "students/student_form.html")


@login_required
def student_update(request, pk):
    return render(request, "students/student_form.html")


@login_required
def student_delete(request, pk):
    return render(request, "students/student_confirm_delete.html")