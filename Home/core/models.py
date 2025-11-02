# core/models.py
from django.db import models
from django.utils import timezone
from django.conf import settings


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.code} - {self.name}"




from django.db import models
from django.utils import timezone
from django.conf import settings

# ======================================
# Teacher Model (Upgraded)
# ======================================

class Teacher(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='teacher_profile'
    )

    # NEW UNIQUE TEACHER ID (e.g., TCH-0001)
    teacher_id = models.CharField(max_length=20, unique=True, blank=True, null=True)

    # Existing fields
    first_name = models.CharField(max_length=50)
    last_name  = models.CharField(max_length=50)
    email      = models.EmailField(unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name="teachers")
    hire_date  = models.DateField(default=timezone.now)

    # New fields (for professional upgrade)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)

    QUALIFICATION_CHOICES = [
        ('BS', 'BS / Bachelor'),
        ('MS', 'MS / Master'),
        ('MPhil', 'MPhil'),
        ('PhD', 'PhD'),
        ('Other', 'Other'),
    ]
    qualification = models.CharField(max_length=50, choices=QUALIFICATION_CHOICES, null=True, blank=True)
    specialization = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField(blank=True, null=True)

    # Additional useful attributes
    experience_years = models.PositiveIntegerField(default=0, help_text="Years of teaching experience")
    contact_number = models.CharField(max_length=20, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.teacher_id:
            prefix = "TCH"
            last_id = Teacher.objects.all().count() + 1
            self.teacher_id = f"{prefix}-{last_id:04d}"  # Example: TCH-0001
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.teacher_id})"


# ======================================
# Student Model (Upgraded)
# ======================================

class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='student_profile'
    )

    # NEW UNIQUE STUDENT ID (e.g., STU-0001)
    student_id = models.CharField(max_length=20, unique=True, blank=True, null=True)

    # Existing fields
    first_name = models.CharField(max_length=50)
    last_name  = models.CharField(max_length=50)
    email      = models.EmailField(unique=True)
    phone      = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    enrollment_date = models.DateField(default=timezone.now)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name="students")

    # Academic info
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    ACADEMIC_BACKGROUND_CHOICES = [
        ('FSc Pre-Medical', 'FSc Pre-Medical'),
        ('FSc Pre-Engineering', 'FSc Pre-Engineering'),
        ('ICS', 'ICS'),
        ('ICom', 'ICom'),
        ('FA', 'FA'),
        ('BA', 'BA'),
        ('BSc', 'BSc'),
        ('Other', 'Other'),
    ]
    academic_background = models.CharField(max_length=50, choices=ACADEMIC_BACKGROUND_CHOICES, null=True, blank=True)

    # New fields (for professional system)
    guardian_name = models.CharField(max_length=100, blank=True, null=True)
    guardian_contact = models.CharField(max_length=20, blank=True, null=True)
    semester = models.PositiveIntegerField(default=1)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.student_id:
            prefix = "STU"
            last_id = Student.objects.all().count() + 1
            self.student_id = f"{prefix}-{last_id:04d}"  # Example: STU-0001
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"



class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    credits = models.PositiveIntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="courses")
    # NEW: which teacher teaches this course (optional so migrations won't demand a default)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name="courses")

    def __str__(self):
        return f"{self.code} - {self.name}"


class Enrollment(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("completed", "Completed"),
        ("dropped", "Dropped"),
    ]

    GRADE_CHOICES = [
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
        ("D", "D"),
        ("F", "F"),
        ("N/A", "Not Graded Yet"),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    # safer default instead of auto_now_add (avoids migration prompt)
    enrollment_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    grade = models.CharField(max_length=5, choices=GRADE_CHOICES, default="N/A")

    class Meta:
        unique_together = ('student', 'course')  # prevent duplicate enrollment

    def __str__(self):
        return f"{self.student} → {self.course}"


# core/models.py  (append near other models)
from django.db import models
from django.conf import settings

# Assumes Course, Enrollment, Student, Teacher already exist above

# in models.py
# new change 
class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(null=True, blank=True)
    total_marks = models.DecimalField(max_digits=5, decimal_places=2, default=10)  # add this
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.title} ({self.course.name})"

# new change date 10/28 
class Mark(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='marks')
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='marks')
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    total_marks = models.DecimalField(max_digits=5, decimal_places=2, default=10)
    graded_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('assignment', 'student')

    def __str__(self):
        return f"{self.student} - {self.assignment}: {self.marks_obtained}/{self.total_marks}"




class Attendance(models.Model):
    enrollment = models.ForeignKey('Enrollment', on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    present = models.BooleanField(default=False)

    class Meta:
        unique_together = ('enrollment', 'date')

    def __str__(self):
        return f"{self.enrollment.student} on {self.date}: {'Present' if self.present else 'Absent'}"
