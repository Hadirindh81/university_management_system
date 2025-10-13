# core/forms_teacher.py
from django import forms
from .models import Assignment, Mark, Attendance

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date']

class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['score']

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['present']
