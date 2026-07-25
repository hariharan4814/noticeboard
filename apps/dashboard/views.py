from django.db.models import Count, Q
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.notices.models import Notice
from apps.students.models import Student


@login_required
def home(request):
    notice_stats = Notice.objects.aggregate(
        total_notices=Count("id"),
        active_notices=Count("id", filter=Q(is_active=True)),
        inactive_notices=Count("id", filter=Q(is_active=False)),
    )

    context = {
        "total_students": Student.objects.count(),
        "total_notices": notice_stats["total_notices"],
        "active_notices": notice_stats["active_notices"],
        "inactive_notices": notice_stats["inactive_notices"],
        "recent_notices": Notice.objects.only(
            "title",
            "notice_type",
            "created_at",
            "is_active",
        ).order_by("-created_at")[:5],
    }

    return render(request, "dashboard/home.html", context)