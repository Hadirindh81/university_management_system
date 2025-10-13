from django.db import models
from core.models import Student   # ✅ Correct import (Student is in core.models)

class Fee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="fees")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    due_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Auto-calculate balance
        self.balance = self.total_amount - self.amount_paid
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Fee for {self.student.first_name} {self.student.last_name}"

