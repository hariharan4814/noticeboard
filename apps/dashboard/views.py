from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.notices.models import Notice


@login_required
def home(request):
    context = {
        "total_notices": Notice.objects.count(),
        "active_notices": Notice.objects.filter(is_active=True).count(),
    }

    return render(request, "dashboard/home.html", context)