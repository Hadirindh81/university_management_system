from django.contrib import admin
from .models import Fee

@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ("student", "total_amount", "amount_paid", "balance", "due_date")
    search_fields = ("student__first_name", "student__last_name", "student__email")
    list_filter = ("due_date",)

