# fees/views.py   # NEW change added the crud for amdin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from core.models import Student
from .models import Fee
from accounts.decorators import role_required


@login_required
@role_required(['admin'])
def fee_list(request):
    """
    Admin view: list all fees (select_related for student for efficiency).
    """
    fees = Fee.objects.select_related('student').all().order_by('-id')
    return render(request, 'fees/fee_list.html', {'fees': fees})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import role_required
from .models import Fee
from .forms import FeeForm


@login_required
@role_required(['admin'])
def fee_create(request):
    """
    Admin can add a new Fee record using a form.
    """
    if request.method == 'POST':
        form = FeeForm(request.POST)
        if form.is_valid():
            fee = form.save(commit=False)
            # Auto-calculate balance before saving
            fee.balance = fee.total_amount - fee.amount_paid
            fee.save()
            messages.success(request, f"Fee for {fee.student} added successfully.")
            return redirect('fee_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = FeeForm()

    return render(request, 'fees/fee_form.html', {'form': form})


@login_required
@role_required(['admin'])
def fee_update(request, pk):
    """
    Admin: Edit an existing fee record.
    """
    fee = get_object_or_404(Fee, pk=pk)

    if request.method == 'POST':
        form = FeeForm(request.POST, instance=fee)
        if form.is_valid():
            fee = form.save(commit=False)
            # Auto calculate balance
            fee.balance = fee.total_amount - fee.amount_paid
            fee.save()
            messages.success(request, "Fee record updated successfully!")
            return redirect('fee_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = FeeForm(instance=fee)

    return render(request, 'fees/fee_form.html', {'form': form})

@login_required
@role_required(['admin'])
def fee_delete(request, pk):
    """
    Admin: Delete a fee record with confirmation.
    """
    fee = get_object_or_404(Fee, pk=pk)

    if request.method == 'POST':
        fee.delete()
        messages.success(request, "Fee record deleted successfully!")
        return redirect('fee_list')

    # Render a confirmation page
    return render(request, 'fees/fee_confirm_delete.html', {'fee': fee})



@login_required
def my_fee(request):
    """
    Student view: show fees for the logged-in student (linked profile or by email fallback).
    """
    student = getattr(request.user, 'student_profile', None)
    if not student and request.user.email:
        student = Student.objects.filter(email__iexact=request.user.email).first()

    if not student:
        messages.warning(request, "No student record found for this account.")
        return render(request, 'fees/my_fee.html', {'fees': [], 'student': None})

    fees = Fee.objects.filter(student=student).order_by('-id')
    return render(request, 'fees/my_fee.html', {'fees': fees, 'student': student})
