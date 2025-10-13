from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages

class RoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    roles = []  # override: e.g. ['admin','teacher']

    def test_func(self):
        role = getattr(self.request.user, 'profile', None) and getattr(self.request.user.profile, 'role', None)
        if role:
            return str(role).lower() in [r.lower() for r in self.roles]
        return False

    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to access that page.")
        return redirect('home')
