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






# ========================
# STUDENTS CRUD
# ========================

@method_decorator(login_required, name='dispatch')
@method_decorator(role_required(['admin', 'teacher']), name='dispatch')
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

        # allow only linked student to see own details
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


# ------- CREATE -------
@method_decorator(login_required, name='dispatch')
@method_decorator(role_required(['admin']), name='dispatch')
class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'core/students/form.html'
    success_url = reverse_lazy('students_list')


# ------- UPDATE -------
@method_decorator(login_required, name='dispatch')
@method_decorator(role_required(['admin']), name='dispatch')
class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'core/students/form.html'
    success_url = reverse_lazy('students_list')


# ------- DELETE -------
@method_decorator(login_required, name='dispatch')
@method_decorator(role_required(['admin']), name='dispatch')
class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'core/students/confirm_delete.html'
    success_url = reverse_lazy('students_list')



# ========================
# TEACHERS CRUD
# ========================

@method_decorator(login_required, name='dispatch')
@method_decorator(role_required(['admin', 'teacher']), name='dispatch')
class TeacherListView(ListView):
    model = Teacher
    template_name = 'core/teachers/list.html'
    context_object_name = 'teachers'


class TeacherDetailView(DetailView):
    model = Teacher
    template_name = 'core/teachers/detail.html'
    context_object_name = 'teacher'


# ------- CREATE -------
@method_decorator(login_required, name='dispatch')
@method_decorator(role_required(['admin']), name='dispatch')
class TeacherCreateView(CreateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'core/teachers/form.html'
    success_url = reverse_lazy('teachers_list')


# ------- UPDATE -------
@method_decorator(login_required, name='dispatch')
@method_decorator(role_required(['admin']), name='dispatch')
class TeacherUpdateView(UpdateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'core/teachers/form.html'
    success_url = reverse_lazy('teachers_list')


# ------- DELETE -------
@method_decorator(login_required, name='dispatch')
@method_decorator(role_required(['admin']), name='dispatch')
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


# ==========================
# CORE / VIEWS.PY
# DASHBOARDS (ADMIN, TEACHER, STUDENT)
# ==========================

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg, F, Value, FloatField, DecimalField
from django.db.models.functions import Coalesce, Cast
from datetime import date, datetime
import json

from accounts.decorators import role_required
from core.models import Student, Teacher, Course, Enrollment, Assignment, Mark, Attendance
from fees.models import Fee
from .forms_teacher import AssignmentForm, MarkForm, AttendanceForm


# ==========================================================
# ADMIN DASHBOARD (FINAL FIXED VERSION)
# ==========================================================
@login_required
@role_required(['admin'])
def admin_dashboard(request):
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_courses = Course.objects.count()
    total_assignments = Assignment.objects.count()
    total_enrollments = Enrollment.objects.count()

    total_paid = Fee.objects.aggregate(
        total=Coalesce(Sum('amount_paid'), Value(0, output_field=DecimalField()))
    )['total'] or 0
    total_outstanding = Fee.objects.aggregate(
        total=Coalesce(Sum('balance'), Value(0, output_field=DecimalField()))
    )['total'] or 0
    pending_fees_count = Fee.objects.filter(balance__gt=0).count()

    # Safe mark field (fixed: using marks_obtained instead of score)
    course_stats = []
    courses = Course.objects.all().order_by('name')
    for c in courses:
        enroll_count = Enrollment.objects.filter(course=c).count()
        total_sessions = Attendance.objects.filter(enrollment__course=c).values('date').distinct().count()
        total_present = Attendance.objects.filter(enrollment__course=c, present=True).count()

        attendance_percent = None
        if total_sessions and enroll_count:
            possible = total_sessions * enroll_count
            if possible:
                attendance_percent = int((total_present / possible) * 100)

        avg_mark = None
        #  FIXED HERE: changed Mark → Marks, and score → marks_obtained
        qs = Mark.objects.filter(assignment__course=c).exclude(marks_obtained__isnull=True)
        if qs.exists():
            avg = qs.aggregate(avg=Avg(Cast(F('marks_obtained'), FloatField())))['avg']
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

    chart_labels_json = json.dumps([f"{cs['code']} {cs['name']}".strip() for cs in course_stats])
    chart_values_json = json.dumps([int(cs['enroll_count']) for cs in course_stats])
    fees_chart_json = json.dumps({
        'collected': float(total_paid),
        'outstanding': float(total_outstanding)
    })

    recent_assignments = Assignment.objects.order_by('-created_at')[:6]
    recent_fees = Fee.objects.order_by('-id')[:6]
    recent_enrollments = Enrollment.objects.order_by('-id')[:6]

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


# ==========================================================
# TEACHER DASHBOARD
# ==========================================================
@login_required
@role_required(['teacher'])
def teacher_dashboard(request):
    teacher = Teacher.objects.filter(user=request.user).first() or \
              Teacher.objects.filter(email__iexact=request.user.email).first()

    if not teacher:
        courses = Course.objects.none()
        enrollments = Enrollment.objects.none()
        total_students = total_assignments = 0
    else:
        courses = Course.objects.filter(teacher=teacher)
        enrollments = Enrollment.objects.filter(course__in=courses).select_related('student')
        total_students = enrollments.values('student').distinct().count()
        total_assignments = Assignment.objects.filter(course__in=courses).count()

    return render(request, 'core/dashboards/teacher.html', {
        'teacher': teacher,
        'courses': courses,
        'enrollments': enrollments,
        'total_students': total_students,
        'total_assignments': total_assignments,
    })


# ------------------ Teacher: Course Detail ------------------
@login_required
@role_required(['teacher'])
def teacher_course_detail(request, pk):
    teacher = Teacher.objects.filter(user=request.user).first() or \
              Teacher.objects.filter(email__iexact=request.user.email).first()

    course = get_object_or_404(Course, pk=pk)
    if not teacher or course.teacher != teacher:
        messages.error(request, "You don't have permission to view this course.")
        return redirect('teacher_dashboard')

    enrollments = Enrollment.objects.filter(course=course).select_related('student')
    assignments = Assignment.objects.filter(course=course).order_by('-created_at')

    return render(request, 'core/dashboards/teacher_course_detail.html', {
        'course': course,
        'enrollments': enrollments,
        'assignments': assignments,
    })


# ------------------ Attendance ------------------
@login_required
@role_required(['teacher'])
def attendance_mark(request, course_pk):
    teacher = Teacher.objects.filter(user=request.user).first() or \
              Teacher.objects.filter(email__iexact=request.user.email).first()

    course = get_object_or_404(Course, pk=course_pk)
    if not teacher or course.teacher != teacher:
        messages.error(request, "You don't have permission to mark attendance.")
        return redirect('teacher_dashboard')

    d = request.GET.get('date')
    the_date = datetime.strptime(d, "%Y-%m-%d").date() if d else date.today()

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
    teacher = Teacher.objects.filter(user=request.user).first() or \
              Teacher.objects.filter(email__iexact=request.user.email).first()

    course = get_object_or_404(Course, pk=course_pk)
    if not teacher or course.teacher != teacher:
        messages.error(request, "You don't have permission to add assignments.")
        return redirect('teacher_dashboard')

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        Assignment.objects.create(course=course, title=title, description=description, due_date=due_date)
        messages.success(request, "Assignment created successfully.")
        return redirect('teacher_course_detail', pk=course.pk)

    return render(request, 'core/dashboards/assignment_form.html', {'course': course})

# ------------------ Marks Update  ------------------
@login_required
@role_required(['teacher'])
def mark_edit(request, assignment_pk, student_pk):
    teacher = Teacher.objects.filter(user=request.user).first() or \
              Teacher.objects.filter(email__iexact=request.user.email).first()

    assignment = get_object_or_404(Assignment, pk=assignment_pk)
    student = get_object_or_404(Student, pk=student_pk)

    #  Security check
    if not teacher or assignment.course.teacher != teacher:
        messages.error(request, "You don't have permission to grade this assignment.")
        return redirect('teacher_dashboard')

    #  Create mark record if not exist
    mark, _ = Mark.objects.get_or_create(
        assignment=assignment,
        student=student,
        defaults={'total_marks': assignment.total_marks or 10}
    )

    if request.method == 'POST':
        marks_input = request.POST.get('marks', '').strip()

        try:
            marks_obtained = float(marks_input)
        except ValueError:
            messages.error(request, "Please enter a valid number for marks.")
            return redirect('mark_edit', assignment_pk=assignment.pk, student_pk=student.pk)

        total_marks = float(getattr(assignment, 'total_marks', 10))
        if marks_obtained > total_marks:
            messages.warning(request, f"Marks cannot exceed total ({total_marks}). Setting to total.")
            marks_obtained = total_marks
        elif marks_obtained < 0:
            marks_obtained = 0

        # Save cleanly
        mark.marks_obtained = marks_obtained
        mark.total_marks = total_marks
        mark.save()

        messages.success(request, f"Marks saved successfully: {marks_obtained}/{total_marks}")
        return redirect('teacher_course_detail', pk=assignment.course.pk)

    return render(request, 'core/dashboards/mark_form.html', {
        'assignment': assignment,
        'student': student,
        'mark': mark,
    })




# ==========================================================
# STUDENT DASHBOARD
# ==========================================================
@login_required
@role_required(['student'])
def student_dashboard(request):
    student = getattr(request.user, 'student_profile', None) or \
              Student.objects.filter(email__iexact=request.user.email).first()

    if not student:
        messages.warning(request, "No student profile linked to your account.")
        return render(request, 'core/dashboards/student.html', {
            'student': None,
            'courses_info': [],
            'fees': [],
            'total_balance': 0,
            'total_courses': 0,
            'avg_attendance': None,
        })

    courses = Course.objects.filter(enrollments__student=student).distinct()
    courses_info, attendance_percents = [], []

    for c in courses:
        assignments = Assignment.objects.filter(course=c).order_by('-created_at')
        assignments_with_marks = []
        for a in assignments:
            mark_obj = Mark.objects.filter(assignment=a, student=student).first()
            assignments_with_marks.append({
                'assignment': a,
                'mark': mark_obj
            })

        total_sessions = Attendance.objects.filter(enrollment__course=c).values('date').distinct().count()
        present_count = Attendance.objects.filter(
            enrollment__course=c, enrollment__student=student, present=True
        ).count()
        percent = int((present_count / total_sessions) * 100) if total_sessions > 0 else None
        if percent:
            attendance_percents.append(percent)

        courses_info.append({
            'course': c,
            'assignments_with_marks': assignments_with_marks,
            'attendance': {
                'total_sessions': total_sessions,
                'present': present_count,
                'percent': percent
            }
        })

    fees = Fee.objects.filter(student=student).order_by('-id')
    total_balance = sum((f.balance or 0) for f in fees)
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


# ==========================================================
# STUDENT COURSE DETAIL
# ==========================================================
@login_required
@role_required(['student'])
def student_course_detail(request, pk):
    student = getattr(request.user, 'student_profile', None) or \
              Student.objects.filter(email__iexact=request.user.email).first()

    course = get_object_or_404(Course, pk=pk)
    enrollment = Enrollment.objects.filter(course=course, student=student).first()
    if not enrollment:
        messages.error(request, "You are not enrolled in this course.")
        return redirect('student_dashboard')

    assignments = Assignment.objects.filter(course=course).order_by('-created_at')
    assignments_with_marks = []
    for a in assignments:
        mark_obj = Mark.objects.filter(assignment=a, student=student).first()
        total = float(getattr(a, 'total_marks', 10))
        obtained = float(mark_obj.marks_obtained) if mark_obj and mark_obj.marks_obtained is not None else None

        if obtained is None:
            status = "Pending"
        elif obtained >= (total / 2):
            status = "Passed"
        else:
            status = "Failed"

        assignments_with_marks.append({
            'assignment': a,
            'mark': mark_obj,
            'status': status,
        })

    attendance_list = Attendance.objects.filter(enrollment=enrollment).order_by('-date')
    fees = Fee.objects.filter(student=student).order_by('-id')

    return render(request, 'core/dashboards/student_course_detail.html', {
        'student': student,
        'course': course,
        'enrollment': enrollment,
        'assignments_with_marks': assignments_with_marks,
        'attendance_list': attendance_list,
        'fees': fees,
    })
