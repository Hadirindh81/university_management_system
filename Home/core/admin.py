
# core/admin.py
from django.contrib import admin
from .models import Department, Teacher, Student, Course, Enrollment

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'department', 'hire_date')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('department',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'department', 'enrollment_date')
    list_filter = ('department',)
    search_fields = ('first_name', 'last_name', 'email')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'department', 'teacher', 'credits')
    list_filter = ('department',)
    search_fields = ('name', 'code')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'status', 'grade', 'enrollment_date')
    list_filter = ('status', 'grade', 'course')
    search_fields = ('student__first_name', 'student__last_name', 'course__name')
