# core/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from accounts.decorators import role_required


# Import models and forms
from .models import Department, Course, Enrollment, Student, Teacher
from .forms import DepartmentForm, CourseForm, EnrollmentForm, StudentForm, TeacherForm


# ======================
# Home + Static Sections
# ======================
def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')

def help(request):
    return render(request, 'core/help.html')

def students(request):
    return render(request, 'core/students.html')

def teachers(request):
    return render(request, 'core/teachers.html')

def courses(request):
    return render(request, 'core/courses.html')

def departments(request):
    return render(request, 'core/departments.html')

def enrollments(request):
    return render(request, 'core/enrollments.html')


# ==============
# Students CRUD
# ==============

@method_decorator(login_required, name='dispatch')
@method_decorator(role_required(['admin','teacher']), name='dispatch')
class StudentListView(ListView):
    model = Student
    template_name = 'core/students/list.html'
    context_object_name = 'students'
    ordering = ['-enrollment_date']
    paginate_by = 25

class StudentDetailView(DetailView):
    model = Student
    template_name = 'core/students/detail.html'
    context_object_name = 'student'

    def dispatch(self, request, *args, **kwargs):
        # allow admin and teacher to access any student
        role = getattr(request.user, 'profile', None) and getattr(request.user.profile, 'role', None)
        role = str(role).lower() if role else None
        if role in ('admin', 'teacher'):
            return super().dispatch(request, *args, **kwargs)

        # if student role → allow only if linked student.user == request.user
        if role == 'student':
            self.object = self.get_object()
            if getattr(self.object, 'user', None) == request.user:
                return super().dispatch(request, *args, **kwargs)

        messages.error(request, "You don't have permission to view that student.")
        return redirect('home')


    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['enrollments'] = self.object.enrollments.select_related(
            'course', 'course__teacher'
        ).all()
        return ctx

@method_decorator(login_required, name='dispatch')
@method_decorator(role_required(['admin']), name='dispatch')
class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'core/students/form.html'
    success_url = reverse_lazy('students_list')

@method_decorator(login_required, name='dispatch')
@method_decorator(role_required(['admin','teacher']), name='dispatch')
class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'core/students/form.html'

    def get_success_url(self):
        return reverse_lazy('student_detail', kwargs={'pk': self.object.pk})

@method_decorator(login_required, name='dispatch')
@method_decorator(role_required(['admin']), name='dispatch')
class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'core/students/confirm_delete.html'
    success_url = reverse_lazy('students_list')


# ==============
# Teachers CRUD
# ==============
class TeacherListView(ListView):
    model = Teacher
    template_name = 'core/teachers/list.html'
    context_object_name = 'teachers'

class TeacherDetailView(DetailView):
    model = Teacher
    template_name = 'core/teachers/detail.html'
    context_object_name = 'teacher'

class TeacherCreateView(CreateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'core/teachers/form.html'
    success_url = reverse_lazy('teachers_list')

class TeacherUpdateView(UpdateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'core/teachers/form.html'
    success_url = reverse_lazy('teachers_list')

class TeacherDeleteView(DeleteView):
    model = Teacher
    template_name = 'core/teachers/confirm_delete.html'
    success_url = reverse_lazy('teachers_list')


# ==============
# Departments CRUD
# ==============
class DepartmentListView(ListView):
    model = Department
    template_name = "core/departments/list.html"
    context_object_name = "departments"
# last change 
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required

@login_required
@role_required(['admin'])

def department_add(request):
    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("department_list")
    else:
        form = DepartmentForm()
    return render(request, "core/departments/form.html", {"form": form})

def department_edit(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == "POST":
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect("department_list")
    else:
        form = DepartmentForm(instance=department)
    return render(request, "core/departments/form.html", {"form": form})

def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == "POST":
        department.delete()
        return redirect("department_list")
    return render(request, "core/departments/confirm_delete.html", {"department": department})


# ==============
# Courses CRUD
# ==============
class CourseListView(ListView):
    model = Course
    template_name = 'core/courses/list.html'
    context_object_name = 'courses'
# last change only admin have access to crud 
from django.utils.decorators import method_decorator
from accounts.decorators import role_required
from django.contrib.auth.decorators import login_required

@method_decorator(login_required, name='dispatch')
@method_decorator(role_required(['admin']), name='dispatch')

class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'core/courses/form.html'
    success_url = reverse_lazy('courses_list')
# step 10 B step2 
@method_decorator(login_required, name='dispatch')
@method_decorator(role_required(['admin','teacher']), name='dispatch')
class CourseUpdateView(UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'core/courses/form.html'
    success_url = reverse_lazy('courses_list')

    def dispatch(self, request, *args, **kwargs):
        role = getattr(request.user, 'profile', None) and getattr(request.user.profile, 'role', None)
        role = role.lower() if role else None

        # Admin allowed
        if role == 'admin':
            return super().dispatch(request, *args, **kwargs)

        # Teacher allowed only if they are the course owner
        if role == 'teacher':
            self.object = self.get_object()
            # self.object.teacher must exist and have .user
            if getattr(self.object, 'teacher', None) and getattr(self.object.teacher, 'user', None) == request.user:
                return super().dispatch(request, *args, **kwargs)

        messages.error(request, "You don't have permission to edit this course.")
        return redirect('home')
    
@method_decorator(login_required, name='dispatch')
@method_decorator(role_required(['admin']), name='dispatch')
class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'core/courses/confirm_delete.html'
    success_url = reverse_lazy('courses_list')

class CourseDetailView(DetailView):
    model = Course
    template_name = 'core/courses/detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['enrollments'] = self.object.enrollments.select_related('student').all()
        return ctx


# ==============
# Enrollments CRUD
# ==============
def enrollments_list(request):
    enrollments = Enrollment.objects.select_related(
        'student', 'course', 'course__teacher'
    ).order_by('-enrollment_date')
    return render(request, 'core/enrollments/list.html', {'enrollments': enrollments})

def enrollment_detail(request, pk):
    enrollment = get_object_or_404(
        Enrollment.objects.select_related('student', 'course', 'course__teacher'), pk=pk
    )
    return render(request, 'core/enrollments/detail.html', {'enrollment': enrollment})

def enrollment_add(request):
    initial = {}
    student_pk = request.GET.get('student')
    course_pk = request.GET.get('course')
    if student_pk:
        try:
            initial['student'] = Student.objects.get(pk=student_pk)
        except Student.DoesNotExist:
            pass
    if course_pk:
        try:
            initial['course'] = Course.objects.get(pk=course_pk)
        except Course.DoesNotExist:
            pass

    if request.method == "POST":
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('enrollments_list')
    else:
        form = EnrollmentForm(initial=initial)

    return render(request, 'core/enrollments/form.html', {'form': form, 'title': 'Add Enrollment'})

def enrollment_edit(request, pk):
    enrollment = get_object_or_404(Enrollment, pk=pk)
    if request.method == "POST":
        form = EnrollmentForm(request.POST, instance=enrollment)
        if form.is_valid():
            form.save()
            return redirect('enrollment_detail', pk=enrollment.pk)
    else:
        form = EnrollmentForm(instance=enrollment)
    return render(request, 'core/enrollments/form.html', {'form': form, 'title': 'Edit Enrollment'})

def enrollment_delete(request, pk):
    enrollment = get_object_or_404(Enrollment, pk=pk)
    if request.method == 'POST':
        enrollment.delete()
        return redirect('enrollments_list')
    return render(request, 'core/enrollments/confirm_delete.html', {'enrollment': enrollment})


# ==========
# Profile
# ==========
@login_required
def profile(request):
    return render(request, 'registration/profile.html')


# ==============
# Role Base Access System
# ==============
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from datetime import date, datetime


from .models import Course, Enrollment, Assignment, Mark, Attendance, Student, Teacher


# ------------ Admin Dashboard -------------
# ------------ Admin Dashboard -------------
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg, F, Value
from django.db.models.functions import Coalesce, Cast
from django.db.models import FloatField, DecimalField
from accounts.decorators import role_required
from core.models import Student, Teacher, Course, Enrollment, Assignment, Mark, Attendance
from fees.models import Fee
import json

@login_required
@role_required(['admin'])
def admin_dashboard(request):
    """
    Enhanced admin dashboard (type-safe, JSON safe).
    """

    # Basic counts
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_courses = Course.objects.count()
    total_assignments = Assignment.objects.count()
    total_enrollments = Enrollment.objects.count()

    # Financials (avoid DecimalField & IntegerField conflict)
    total_paid = Fee.objects.aggregate(
        total=Coalesce(Sum('amount_paid'), Value(0, output_field=DecimalField()))
    )['total'] or 0

    total_outstanding = Fee.objects.aggregate(
        total=Coalesce(Sum('balance'), Value(0, output_field=DecimalField()))
    )['total'] or 0

    pending_fees_count = Fee.objects.filter(balance__gt=0).count()

    # Figure out mark field name dynamically
    mark_field = None
    for f in Mark._meta.get_fields():
        if getattr(f, 'name', None) in ('score', 'marks'):
            mark_field = f.name
            break

    # Per-course stats
    course_stats = []
    courses = Course.objects.all().order_by('name')
    for c in courses:
        enroll_count = Enrollment.objects.filter(course=c).count()

        # Attendance stats
        total_sessions = Attendance.objects.filter(enrollment__course=c).values('date').distinct().count()
        total_present = Attendance.objects.filter(enrollment__course=c, present=True).count()

        attendance_percent = None
        if total_sessions and enroll_count:
            possible = total_sessions * enroll_count
            if possible:
                attendance_percent = int((total_present / possible) * 100)

        # Average marks
        avg_mark = None
        if mark_field:
            qs = Mark.objects.filter(assignment__course=c).exclude(**{f'{mark_field}__isnull': True})
            if qs.exists():
                avg = qs.aggregate(avg=Avg(Cast(F(mark_field), FloatField())))['avg']
                if avg is not None:
                    avg_mark = round(float(avg), 2)

        course_stats.append({
            'id': c.id,
            'code': getattr(c, 'code', '') or '',
            'name': c.name,
            'enroll_count': enroll_count,
            'attendance_percent': attendance_percent,
            'avg_mark': avg_mark,
        })

    #  Prepare chart data safely for JSON
    chart_labels = [f"{cs['code']} {cs['name']}".strip() for cs in course_stats]
    chart_values = [int(cs['enroll_count']) for cs in course_stats]

    fees_chart = {
        'collected': float(total_paid) if total_paid is not None else 0.0,
        'outstanding': float(total_outstanding) if total_outstanding is not None else 0.0,
    }

    # JSON-safe serialization for template
    chart_labels_json = json.dumps(chart_labels)
    chart_values_json = json.dumps(chart_values)
    fees_chart_json = json.dumps(fees_chart)

    #  Define these BEFORE context
    recent_assignments = Assignment.objects.order_by('-created_at')[:6]
    recent_fees = Fee.objects.order_by('-id')[:6]
    recent_enrollments = Enrollment.objects.order_by('-id')[:6]

    #  Now safely build the context
    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_courses': total_courses,
        'total_assignments': total_assignments,
        'total_enrollments': total_enrollments,
        'total_paid': total_paid,
        'total_outstanding': total_outstanding,
        'pending_fees_count': pending_fees_count,
        'course_stats': course_stats,
        'chart_labels_json': chart_labels_json,
        'chart_values_json': chart_values_json,
        'fees_chart_json': fees_chart_json,
        'recent_assignments': recent_assignments,
        'recent_fees': recent_fees,
        'recent_enrollments': recent_enrollments,
    }

    return render(request, 'core/dashboards/admin.html', context)

# Last change of replacing the old dashboard with the error to this one # contain path errorcd
@login_required
@role_required(['teacher'])
def teacher_dashboard(request):
    # Try linked teacher first
    teacher = Teacher.objects.filter(user=request.user).first()
    if not teacher and request.user.email:
        teacher = Teacher.objects.filter(email__iexact=request.user.email).first()

    if not teacher:
        courses = Course.objects.none()
        enrollments = Enrollment.objects.none()
        total_students = 0
        total_assignments = 0
    else:
        courses = Course.objects.filter(teacher=teacher)
        enrollments = Enrollment.objects.filter(course__in=courses).select_related('student')
        # distinct students count across courses
        total_students = Enrollment.objects.filter(course__in=courses).values('student').distinct().count()
        total_assignments = Assignment.objects.filter(course__in=courses).count()

    return render(request, 'core/dashboards/teacher.html', {
        'teacher': teacher,
        'courses': courses,
        'enrollments': enrollments,
        'total_students': total_students,
        'total_assignments': total_assignments,
    })







#step 11 Teacher dashboard updates + polish 

# core/views.py  (append under existing dashboards)
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from .models import Course, Enrollment, Assignment, Mark, Attendance, Student, Teacher
from .forms_teacher import AssignmentForm, MarkForm, AttendanceForm
from django.views.decorators.http import require_http_methods

# Teacher: list of their courses
@login_required
@role_required(['teacher'])
def teacher_courses(request):
    teacher = Teacher.objects.filter(user=request.user).first()
    if not teacher:
        # fallback: attempt match by email
        teacher = Teacher.objects.filter(email__iexact=request.user.email).first()

    courses = Course.objects.filter(teacher=teacher) if teacher else Course.objects.none()
    return render(request, 'core/teacher/courses_list.html', {'courses': courses, 'teacher': teacher})


# Course detail: enrolled students, assignments
# inside core/views.py (replace existing teacher_course_detail)
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
@login_required
@role_required(['teacher'])
def teacher_course_detail(request, pk):
    # find teacher linked to request.user, fallback to email
    teacher = Teacher.objects.filter(user=request.user).first()
    if not teacher and request.user.email:
        teacher = Teacher.objects.filter(email__iexact=request.user.email).first()

    course = get_object_or_404(Course, pk=pk)

    # ownership check (by pk or fallback to email)
    is_owner = False
    if teacher and course.teacher:
        if getattr(course.teacher, 'pk', None) == getattr(teacher, 'pk', None):
            is_owner = True
        else:
            t_email = getattr(course.teacher, 'email', '') or ''
            u_email = getattr(request.user, 'email', '') or ''
            if t_email.strip().lower() and u_email.strip().lower() and t_email.strip().lower() == u_email.strip().lower():
                is_owner = True

    if not is_owner:
        messages.error(request, "You don't have permission to view that course.")
        return redirect('teacher_dashboard')

    enrollments = Enrollment.objects.filter(course=course).select_related('student')
    assignments = Assignment.objects.filter(course=course).order_by('-created_at')

    return render(request, 'core/dashboards/teacher_course_detail.html', {
        'course': course,
        'enrollments': enrollments,
        'assignments': assignments,
    })




# Create assignment
# ------------------ Attendance ------------------
@login_required
@role_required(['teacher'])
def attendance_mark(request, course_pk):
    teacher = Teacher.objects.filter(user=request.user).first()
    if not teacher and request.user.email:
        teacher = Teacher.objects.filter(email__iexact=request.user.email).first()

    course = get_object_or_404(Course, pk=course_pk)

    if not teacher or course.teacher != teacher:
        messages.error(request, "You don't have permission to mark attendance for this course.")
        return redirect('teacher_dashboard')

    d = request.GET.get('date')
    if d:
        try:
            the_date = datetime.strptime(d, "%Y-%m-%d").date()
        except Exception:
            the_date = date.today()
    else:
        the_date = date.today()

    enrollments = Enrollment.objects.filter(course=course).select_related('student')
    existing = Attendance.objects.filter(enrollment__in=enrollments, date=the_date)
    present_ids = [a.enrollment_id for a in existing if a.present]

    if request.method == 'POST':
        for e in enrollments:
            present_flag = request.POST.get(f'present_{e.pk}') == 'on'
            attendance, _ = Attendance.objects.get_or_create(enrollment=e, date=the_date)
            attendance.present = present_flag
            attendance.save()
        messages.success(request, "Attendance saved.")
        return redirect('teacher_course_detail', pk=course.pk)

    return render(request, 'core/dashboards/attendance_form.html', {
        'course': course,
        'enrollments': enrollments,
        'date': the_date,
        'present_ids': present_ids,
    })


# ------------------ Assignment Create ------------------
@login_required
@role_required(['teacher'])
def assignment_create(request, course_pk):
    teacher = Teacher.objects.filter(user=request.user).first()
    if not teacher and request.user.email:
        teacher = Teacher.objects.filter(email__iexact=request.user.email).first()

    course = get_object_or_404(Course, pk=course_pk)

    if not teacher or course.teacher != teacher:
        messages.error(request, "You don't have permission to add assignments for this course.")
        return redirect('teacher_dashboard')

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        Assignment.objects.create(course=course, title=title, description=description, due_date=due_date)
        messages.success(request, "Assignment created.")
        return redirect('teacher_course_detail', pk=course.pk)

    return render(request, 'core/dashboards/assignment_form.html', {'course': course})


# ------------------ Marks ------------------
@login_required
@role_required(['teacher'])
def mark_edit(request, assignment_pk, student_pk):
    teacher = Teacher.objects.filter(user=request.user).first()
    if not teacher and request.user.email:
        teacher = Teacher.objects.filter(email__iexact=request.user.email).first()

    assignment = get_object_or_404(Assignment, pk=assignment_pk)
    student = get_object_or_404(Student, pk=student_pk)

    if not teacher or assignment.course.teacher != teacher:
        messages.error(request, "You don't have permission to grade this assignment.")
        return redirect('teacher_dashboard')

    mark, created = Mark.objects.get_or_create(assignment=assignment, student=student)

    if request.method == 'POST':
        try:
            mark_value = float(request.POST.get('marks', 0))
        except ValueError:
            mark_value = 0
        mark.marks = mark_value
        mark.save()
        messages.success(request, "Marks updated.")
        return redirect('teacher_course_detail', pk=assignment.course.pk)

    return render(request, 'core/dashboards/mark_form.html', {
        'assignment': assignment,
        'student': student,
        'mark': mark,
    })



# ---------- Student dashboard -----------

# core/views.py (add/replace the student dashboard views section)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required

from .models import Student, Course, Enrollment, Assignment, Mark, Attendance
from fees.models import Fee


@login_required
@role_required(['student'])
def student_dashboard(request):
    """
    Student dashboard: shows enrolled courses, marks preview, attendance summary and fee summary.
    Builds `courses_info` list so templates don't need custom filters.
    """
    # find linked student (OneToOne) or fallback by email
    student = getattr(request.user, 'student_profile', None)
    if not student and request.user.email:
        student = Student.objects.filter(email__iexact=request.user.email).first()

    if not student:
        messages.warning(request, "No student profile linked to your account. Contact admin.")
        return render(request, 'core/dashboards/student.html', {
            'student': None,
            'courses_info': [],
            'fees': [],
            'total_balance': 0,
            'total_courses': 0,
            'avg_attendance': None,
        })

    # enrolled courses via Enrollment relationship
    courses = Course.objects.filter(enrollments__student=student).distinct()

    # Build course info objects for templates
    courses_info = []
    attendance_percents = []
    for c in courses:
        # assignments and student's marks (latest first)
        assignments = Assignment.objects.filter(course=c).order_by('-created_at')
        assignments_with_marks = []
        for a in assignments:
            mark_obj = Mark.objects.filter(assignment=a, student=student).first()
            assignments_with_marks.append({
                'assignment': a,
                'mark': mark_obj
            })

        # attendance summary for this course (distinct session dates)
        total_sessions = Attendance.objects.filter(enrollment__course=c).values('date').distinct().count()
        present_count = Attendance.objects.filter(enrollment__course=c, enrollment__student=student, present=True).count()
        percent = None
        if total_sessions > 0:
            percent = int((present_count / total_sessions) * 100)
            attendance_percents.append(percent)

        courses_info.append({
            'course': c,
            'assignments_with_marks': assignments_with_marks,   # list (may be empty)
            'attendance': {
                'total_sessions': total_sessions,
                'present': present_count,
                'percent': percent
            }
        })

    # Fees for this student
    fees = Fee.objects.filter(student=student).order_by('-id')
    # compute totals (safe handling if Decimal)
    total_balance = sum((f.balance or 0) for f in fees)

    # overall stats
    total_courses = courses.count()
    avg_attendance = int(sum(attendance_percents) / len(attendance_percents)) if attendance_percents else None

    return render(request, 'core/dashboards/student.html', {
        'student': student,
        'courses_info': courses_info,
        'fees': fees,
        'total_balance': total_balance,
        'total_courses': total_courses,
        'avg_attendance': avg_attendance,
    })

# ---------- Student course detail ----------

# ---------- Student course detail ----------

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from core.models import Course, Enrollment, Student, Attendance, Assignment, Mark


@login_required
@role_required(['student'])
def student_course_detail(request, pk):
    """
    Student course detail page:
    - Shows assignments with student's marks
    - Attendance history
    - Linked fee information
    """

    # find linked student profile
    student = getattr(request.user, 'student_profile', None)
    if not student and request.user.email:
        student = Student.objects.filter(email__iexact=request.user.email).first()

    course = get_object_or_404(Course, pk=pk)

    # ensure student is enrolled
    enrollment = Enrollment.objects.filter(course=course, student=student).first()
    if not enrollment:
        messages.error(request, "You are not enrolled in this course.")
        return redirect('student_dashboard')

    # assignments + student's marks
    assignments = Assignment.objects.filter(course=course).order_by('-created_at')
    assignments_with_marks = []
    for a in assignments:
        mark_obj = Mark.objects.filter(assignment=a, student=student).first()
        assignments_with_marks.append({'assignment': a, 'mark': mark_obj})

    # attendance list for this enrollment (ordered desc)
    attendance_list = Attendance.objects.filter(enrollment=enrollment).order_by('-date')

    # student fees (optional link to same student)
    fees = Fee.objects.filter(student=student).order_by('-id')

    return render(request, 'core/dashboards/student_course_detail.html', {
        'student': student,
        'course': course,
        'enrollment': enrollment,
        'assignments_with_marks': assignments_with_marks,
        'attendance_list': attendance_list,
        'fees': fees,
    })
