from django import forms
from .models import Fee


class FeeForm(forms.ModelForm):
    class Meta:
        model = Fee
        fields = ["student", "total_amount", "amount_paid", "due_date"]
        widgets = {
            "student": forms.Select(attrs={"class": "form-control"}),
            "total_amount": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter total fee amount"}),
            "amount_paid": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter amount paid"}),
            "due_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }

    def clean(self):
        """
        Custom validation: ensure amount_paid is not greater than total_amount.
        """
        cleaned_data = super().clean()
        total = cleaned_data.get("total_amount")
        paid = cleaned_data.get("amount_paid")

        if total is not None and paid is not None and paid > total:
            raise forms.ValidationError("Amount paid cannot be greater than total amount.")

        return cleaned_data
