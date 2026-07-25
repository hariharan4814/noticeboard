from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Notice
from .forms import NoticeForm
from django.shortcuts import get_object_or_404

@login_required
def notice_list(request):
    query = request.GET.get("q")
    notice_type = request.GET.get("type")

    notices = Notice.objects.all()

    if query:
        notices = notices.filter(title__icontains=query)

    if notice_type:
        notices = notices.filter(notice_type=notice_type)

    return render(
        request,
        "notices/notice_list.html",
        {
            "notices": notices,
            "query": query,
            "selected_type": notice_type,
            "notice_types": Notice.NOTICE_TYPES,
        },
    )


@login_required
def notice_create(request):
    if request.method == "POST":
        form = NoticeForm(request.POST, request.FILES)

        if form.is_valid():
            notice = form.save(commit=False)
            notice.created_by = request.user
            notice.save()

            return redirect("notice_list")

    else:
        form = NoticeForm()

    return render(
        request,
        "notices/notice_form.html",
        {"form": form},
    )




@login_required
def notice_update(request, pk):
    notice = get_object_or_404(Notice, pk=pk)

    if request.method == "POST":
        form = NoticeForm(request.POST, request.FILES, instance=notice)

        if form.is_valid():
            form.save()
            return redirect("notice_list")
    else:
        form = NoticeForm(instance=notice)

    return render(
        request,
        "notices/notice_form.html",
        {"form": form},
    )


@login_required
def notice_delete(request, pk):
    notice = get_object_or_404(Notice, pk=pk)

    if request.method == "POST":
        notice.delete()
        return redirect("notice_list")

    return render(
        request,
        "notices/notice_confirm_delete.html",
        {"notice": notice},
    )

@login_required
def notice_detail(request, pk):
    notice = get_object_or_404(Notice, pk=pk)

    return render(
        request,
        "notices/notice_detail.html",
        {"notice": notice},
    )