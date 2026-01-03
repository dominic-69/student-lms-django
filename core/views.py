from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist



from .models import Course, Enrollment, Note, LeaveRequest, Profile





#decoratrr
def admin_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.is_staff:
            return view_func(request, *args, **kwargs)
        messages.error(request, "Admin access only")
        return redirect('dashboard')
    return wrapper


#home notesssssss
def home(request):
    recent_notes = (
        Note.objects
        .select_related('student', 'course')
        .order_by('-created_at')[:5]
    )

    return render(request, 'home.html', {
        'recent_notes': recent_notes
    })
    
#to saw the note

@login_required
def view_note(request, note_id):
    note = get_object_or_404(
        Note,
        id=note_id,
        student=request.user  #ownn note see  
    )

    return render(request, 'view_note.html', {
        'note': note
    })


#log inn with main id and passsssssss
def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return redirect('login')

        if not user_obj.is_active:
            messages.error(request, "Your account is blocked. Contact admin.")
            return redirect('login')

        user = authenticate(
            request,
            username=user_obj.username,
            password=password
        )

        if user:
            login(request, user)
            return redirect('dashboard')

        messages.error(request, "Invalid email or password")
        return redirect('login')

    return render(request, 'login.html')
#blockk
# use tryy catchh for [get_object_or_404]

def toggle_user_status(request, user_id):
    try:
        user = User.objects.get(id=user_id, is_staff=False)

        user.is_active = not user.is_active
        user.save()

        if user.is_active:
            messages.success(request, f"{user.username} has been unblocked")
        else:
            messages.success(request, f"{user.username} has been blocked")

    except ObjectDoesNotExist:
        messages.error(request, "User not found or cannot be modified")

    except Exception as e:
        messages.error(request, "Something went wrong. Please try again.")

    return redirect('admin_dashboard')



#loggg outtttttttt
@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


# registerrr logic
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        p1 = request.POST.get('password1')
        p2 = request.POST.get('password2')

        if p1 != p2:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=p1
        )

        Profile.objects.create(user=user)

        login(request, user)
        messages.success(request, "Account created successfully")
        return redirect('dashboard')

    return render(request, 'register.html')

#stdent details to saw admin
@admin_required
def admin_student_detail(request, user_id):
    student = get_object_or_404(User, id=user_id, is_staff=False)

    profile = Profile.objects.filter(user=student).first()
    courses = Course.objects.filter(enrollment__student=student)
    notes = Note.objects.filter(student=student)
    leaves = LeaveRequest.objects.filter(student=student)

    return render(request, 'admin/student_detail.html', {
        'student': student,
        'profile': profile,
        'courses': courses,
        'notes': notes,
        'leaves': leaves,
    })




# dashboard stdnt
@login_required
def dashboard(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')

    courses = Course.objects.filter(enrollment__student=request.user)
    available_courses = Course.objects.exclude(enrollment__student=request.user)

    notes = (
        Note.objects
        .filter(student=request.user)
        .select_related('course')
        .order_by('-created_at')
    )

    leaves = LeaveRequest.objects.filter(student=request.user)

    return render(request, 'dashboard.html', {
        'courses': courses,
        'available_courses': available_courses,
        'notes': notes,
        'leaves': leaves,
    })

@login_required
def home(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')

    courses = Course.objects.filter(enrollment__student=request.user)
    available_courses = Course.objects.exclude(enrollment__student=request.user)

    notes = (
        Note.objects
        .filter(student=request.user)
        .select_related('course')
        .order_by('-created_at')
    )

    leaves = LeaveRequest.objects.filter(student=request.user)

    return render(request, 'home.html', {
        'courses': courses,
        'available_courses': available_courses,
        'notes': notes,
        'leaves': leaves,
    })

# student detaila(settings)
@login_required
def settings_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        request.user.username = request.POST.get('username')
        request.user.email = request.POST.get('email')

        profile.school = request.POST.get('school')
        profile.college = request.POST.get('college')
        profile.bio = request.POST.get('bio')

        request.user.save()
        profile.save()

        messages.success(request, "Profile updated successfully")
        return redirect('home') 

    return render(request, 'settings.html', {'profile': profile})


# =admin dashborad
@admin_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html', {
        'students': User.objects.filter(is_staff=False).select_related('profile'),
        'courses': Course.objects.all(),
        'notes': Note.objects.select_related('student', 'course').order_by('-created_at'),
        'leaves': LeaveRequest.objects.all(),
    })


# admin add courseeeee
@admin_required
def add_course(request):
    if request.method == "POST":
        Course.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description')
        )
        messages.success(request, "Course added successfully")
        return redirect('admin_dashboard')

    return render(request, 'admin/add_course.html')


# enroll course
@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    Enrollment.objects.get_or_create(student=request.user, course=course)
    messages.success(request, f"You enrolled in {course.title}")
    return redirect('dashboard')


# crud for notee
@login_required
def add_note(request):
    if request.method == "POST":
        course = get_object_or_404(
            Course,
            id=request.POST.get('course'),
            enrollment__student=request.user
        )

        Note.objects.create(
            student=request.user,
            course=course,
            title=request.POST.get('title'),
            content=request.POST.get('content')
        )

        messages.success(request, "Note added successfully")
        return redirect('dashboard')

    courses = Course.objects.filter(enrollment__student=request.user)
    return render(request, 'add_note.html', {'courses': courses})


@login_required
def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, student=request.user)

    if request.method == "POST":
        note.title = request.POST.get('title')
        note.content = request.POST.get('content')
        note.save()
        messages.success(request, "Note updated")
        return redirect('dashboard')

    return render(request, 'edit_note.html', {'note': note})


@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, student=request.user)

    if request.method == "POST":
        note.delete()
        messages.success(request, "Note deleted")
        return redirect('dashboard')

    return render(request, 'delete_note.html', {'note': note})


# leave req of student
@login_required
def apply_leave(request):
    if request.method == "POST":
        LeaveRequest.objects.create(
            student=request.user,
            reason=request.POST.get('reason'),
            from_date=request.POST.get('from_date'),
            to_date=request.POST.get('to_date')
        )
        messages.success(request, "Leave request submitted")
        return redirect('dashboard')

    return render(request, 'apply_leave.html')


# leeave req
@admin_required
def admin_leave_requests(request):
    leaves_qs = (
        LeaveRequest.objects
        .select_related('student')
        .order_by('-applied_at')
    )

    paginator = Paginator(leaves_qs, 5) 
    page_number = request.GET.get('page')
    leaves = paginator.get_page(page_number)

    return render(request, 'admin/leave_requests.html', {
        'leaves': leaves
    })




# apprve or rejecfttt

@admin_required
def update_leave_status(request, leave_id, status):
    leave = get_object_or_404(LeaveRequest, id=leave_id)
    status = status.upper()

    if status in ['APPROVED', 'REJECTED']:
        leave.status = status
        leave.save()
        messages.success(request, f"Leave {status.lower()}")

    return redirect('admin_leave_requests')


