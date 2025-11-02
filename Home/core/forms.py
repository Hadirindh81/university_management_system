from django import forms
from .models import Student, Teacher, Department, Course

from django import forms
from .models import Student, Teacher

# ------------------------------
#  STUDENT FORM
# ------------------------------
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'student_id',   #  Read-only unique ID
            'first_name', 'last_name', 'email', 'phone',
            'date_of_birth', 'address', 'department',
            'academic_background', 'semester', 'cgpa',
            'guardian_name', 'guardian_contact', 'profile_image'
        ]
        widgets = {
            'student_id': forms.TextInput(attrs={
                'class': 'form-control', 'readonly': 'readonly'
            }),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={
                'type': 'date', 'class': 'form-control'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3
            }),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'academic_background': forms.Select(
                choices=[
                    ('', 'Select Background'),
                    ('F.Sc Pre-Medical', 'F.Sc Pre-Medical'),
                    ('F.Sc Pre-Engineering', 'F.Sc Pre-Engineering'),
                    ('ICS', 'ICS'),
                    ('FA', 'FA'),
                    ('I.Com', 'I.Com'),
                    ('A-Levels', 'A-Levels'),
                    ('BA/BSc', 'BA/BSc'),
                    ('BS', 'BS'),
                    ('Other', 'Other'),
                ],
                attrs={'class': 'form-select'}
            ),
            'semester': forms.NumberInput(attrs={
                'class': 'form-control', 'min': 1
            }),
            'cgpa': forms.NumberInput(attrs={
                'class': 'form-control', 'step': '0.01', 'placeholder': 'e.g., 3.45'
            }),
            'guardian_name': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Guardian full name'
            }),
            'guardian_contact': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'e.g., 0300-1234567'
            }),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Optional fields setup
        self.fields['department'].required = False
        self.fields['profile_image'].required = False
        self.fields['guardian_name'].required = False
        self.fields['guardian_contact'].required = False
        self.fields['cgpa'].required = False

        # Prefill the student_id if editing an existing record
        if self.instance and self.instance.pk:
            self.fields['student_id'].initial = self.instance.student_id

# ------------------------------
#  TEACHER FORM
# ------------------------------
# ------------------------------
#  TEACHER FORM
# ------------------------------
class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = [
            'teacher_id',  # read-only ID
            'first_name', 'last_name', 'email',
            'contact_number', 'department', 'hire_date',
            'qualification', 'specialization',
            'experience_years', 'bio', 'profile_image'
        ]
        widgets = {
            'teacher_id': forms.TextInput(attrs={
                'class': 'form-control', 'readonly': 'readonly'
            }),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'hire_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'qualification': forms.Select(
                choices=[
                    ('', 'Select Qualification'),
                    ('BS', 'BS / Bachelor'),
                    ('MS', 'MS / Master'),
                    ('MPhil', 'MPhil'),
                    ('PhD', 'PhD'),
                    ('Other', 'Other'),
                ],
                attrs={'class': 'form-select'}
            ),
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write short biography...'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_image'].required = False
        # Show existing ID if editing
        if self.instance and self.instance.pk:
            self.fields['teacher_id'].initial = self.instance.teacher_id

# core/forms.py  (append these)
from django import forms
from .models import Department, Course, Enrollment

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'code', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'description', 'credits', 'department', 'teacher']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'credits': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'teacher': forms.Select(attrs={'class': 'form-select'}),
        }


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'status', 'grade']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'course': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'grade': forms.Select(attrs={'class': 'form-select'}),
        }
