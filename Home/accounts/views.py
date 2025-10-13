# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from .forms import RegisterForm, UserUpdateForm
from core.models import Student, Teacher   # <-- add this import


def _role_dashboard_url_for(user):
    """Return the appropriate dashboard URL (reverse_lazy) for a user by role."""
    try:
        role = getattr(user, "profile", None) and getattr(user.profile, "role", None)
        role = role.lower() if role else None
    except Exception:
        role = None

    if role == "admin":
        return reverse_lazy("admin_dashboard")
    if role == "teacher":
        return reverse_lazy("teacher_dashboard")
    if role == "student":
        return reverse_lazy("student_dashboard")
    return reverse_lazy("home")


#  Updated Registration view
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get("role")
            email = form.cleaned_data.get("email")

            # Link or create Student/Teacher record
            if role.lower() == "teacher":
                teacher, created = Teacher.objects.get_or_create(
                    email=email,
                    defaults={"user": user, "first_name": user.first_name, "last_name": user.last_name}
                )
                if not created:  # teacher already existed
                    teacher.user = user
                    teacher.save()

            elif role.lower() == "student":
                student, created = Student.objects.get_or_create(
                    email=email,
                    defaults={"user": user, "first_name": user.first_name, "last_name": user.last_name}
                )
                if not created:  # student already existed
                    student.user = user
                    student.save()

            # auto-login after registration
            login(request, user)
            messages.success(request, "Registration successful. Welcome!")
            return redirect(_role_dashboard_url_for(user))
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})



# Role-based LoginView (uses Django's LoginView, but redirects by role)
class RoleBasedLoginView(LoginView):
    template_name = "registration/login.html"

    def get_success_url(self):
        return _role_dashboard_url_for(self.request.user)


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("login")


@login_required
def profile_view(request):
    return render(request, "registration/profile.html")


@login_required
def edit_profile_view(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, "registration/edit_profile.html", {"form": form})
