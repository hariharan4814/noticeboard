from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from apps.common.decorators import staff_or_superuser_required
from .forms import StudentForm
from .models import Student


@login_required
def student_list(request):
    students = Student.objects.all().order_by("roll_number")

    query = request.GET.get("q", "").strip()
    department = request.GET.get("department", "").strip()
    year = request.GET.get("year", "").strip()

    if query:
        students = students.filter(
            Q(name__icontains=query) | Q(roll_number__icontains=query)
        )

    if department:
        students = students.filter(department=department)

    if year:
        students = students.filter(year=year)

    paginator = Paginator(students, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    departments = Student.objects.order_by("department").values_list(
        "department", flat=True
    ).distinct()

    return render(
        request,
        "students/student_list.html",
        {
            "students": page_obj,
            "query": query,
            "selected_department": department,
            "selected_year": year,
            "departments": departments,
            "year_choices": Student.YEAR_CHOICES,
        },
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
@staff_or_superuser_required
def student_create(request):
    if request.method == "POST":
        form = StudentForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Student Added Successfully.")
            return redirect("students:student_list")

    else:
        form = StudentForm()

    return render(
        request,
        "students/student_form.html",
        {
            "form": form,
            "title": "Add Student",
            "button_label": "Save Student",
        },
    )


@login_required
@staff_or_superuser_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)

        if form.is_valid():
            updated_student = form.save()
            messages.success(request, "Student Updated Successfully.")
            return redirect("students:student_detail", pk=updated_student.pk)

    else:
        form = StudentForm(instance=student)

    return render(
        request,
        "students/student_form.html",
        {
            "form": form,
            "student": student,
            "title": "Edit Student",
            "button_label": "Update Student",
        },
    )


@login_required
@staff_or_superuser_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == "POST":
        student_name = student.name
        student.delete()
        messages.success(request, f"Student Deleted Successfully. ({student_name})")
        return redirect("students:student_list")

    return render(
        request,
        "students/student_confirm_delete.html",
        {"student": student},
    )