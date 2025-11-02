
# core/admin.py
from django.contrib import admin
from .models import Department, Teacher, Student, Course, Enrollment
# -------------------- Deparment ADMIN --------------------
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')



# -------------------- TEACHER ADMIN --------------------
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        'teacher_id',
        'first_name',
        'last_name',
        'email',
        'contact_number',
        'qualification',
        'specialization',
        'department',
        'experience_years',
        'hire_date',
    )

    search_fields = (
        'teacher_id', 'first_name', 'last_name',
        'email', 'specialization', 'department__name'
    )

    list_filter = (
        'qualification', 'department', 'hire_date'
    )

    readonly_fields = ('teacher_id', 'profile_image_preview')

    fieldsets = (
        ('Basic Information', {
            'fields': (
                'teacher_id',
                'first_name',
                'last_name',
                'email',
                'contact_number',
                'department',
                'hire_date',
            )
        }),
        ('Professional Details', {
            'fields': (
                'qualification',
                'specialization',
                'experience_years',
                'bio',
            )
        }),
        ('Profile Image', {
            'fields': ('profile_image', 'profile_image_preview'),
        }),
    )

    def profile_image_preview(self, obj):
        if obj.profile_image:
            return f'<img src="{obj.profile_image.url}" width="80" height="80" style="border-radius:50%; object-fit:cover;" />'
        return "No Image"

    profile_image_preview.allow_tags = True
    profile_image_preview.short_description = "Profile Image Preview"



# -------------------- STUDENT ADMIN --------------------
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'student_id', 'first_name', 'last_name', 'email',
        'phone', 'department', 'semester', 'cgpa'
    )
    list_filter = ('department', 'semester')
    search_fields = ('first_name', 'last_name', 'email', 'student_id')
    readonly_fields = ('student_id',)
    fieldsets = (
        ('Basic Info', {
            'fields': ('student_id', 'first_name', 'last_name', 'email', 'phone', 'profile_image')
        }),
        ('Academic Info', {
            'fields': ('department', 'academic_background', 'semester', 'cgpa')
        }),
        ('Personal Details', {
            'fields': ('date_of_birth', 'address')
        }),
        ('Guardian Info', {
            'fields': ('guardian_name', 'guardian_contact')
        }),
    )

    #  Display profile image preview in admin detail view
    def profile_image_preview(self, obj):
        if obj.profile_image:
            return f'<img src="{obj.profile_image.url}" width="80" height="80" style="border-radius:50%; object-fit:cover;" />'
        return "No Image"

    profile_image_preview.allow_tags = True
    profile_image_preview.short_description = "Profile Image Preview"


# -------------------- Course --------------------
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'department', 'teacher', 'credits')
    list_filter = ('department',)
    search_fields = ('name', 'code')
# --------------------  Enrollment  --------------------
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'status', 'grade', 'enrollment_date')
    list_filter = ('status', 'grade', 'course')
    search_fields = ('student__first_name', 'student__last_name', 'course__name')
