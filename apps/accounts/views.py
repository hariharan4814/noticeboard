from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:
            login(request, user)

            if user.role == "ADMIN":
                return redirect("home")

            return redirect("home")

        messages.error(request, "Invalid username or password.")

    return render(request, "registration/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")