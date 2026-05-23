from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.db.models import Count
from .models import Student

# 👉 LOGIN
def login_view(request):
    next_url = request.POST.get('next') or request.GET.get('next') or reverse('students:student_list')

    if request.user.is_authenticated:
        if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
            return redirect(next_url)
        return redirect('students:student_list')

    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect('students:student_list')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'students/login.html', {'next': next_url})

# 👉 LOGOUT
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('students:login')

# 👉 SHOW LIST
@login_required(login_url='students:login')
def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/list.html', {'students': students})

# 👉 TOTAL STUDENTS PAGE
@login_required(login_url='students:login')
def total_students(request):
    students = Student.objects.all()
    return render(request, 'students/total_students.html', {
        'students': students,
        'student_count': students.count(),
    })

# 👉 CLASS RECORDS PAGE
@login_required(login_url='students:login')
def class_records(request):
    courses = (
        Student.objects
        .values('course')
        .annotate(total=Count('id'))
        .order_by('course')
    )
    return render(request, 'students/class_records.html', {'courses': courses})

# 👉 EDIT WORKFLOW PAGE
@login_required(login_url='students:login')
def edit_workflow(request):
    students = Student.objects.all()
    return render(request, 'students/edit_workflow.html', {'students': students})

# 👉 ADD STUDENT
@login_required(login_url='students:login')
def add_student(request):
    if request.method == "POST":
        name = request.POST['name']
        age = request.POST['age']
        course = request.POST['course']

        Student.objects.create(
            name=name,
            age=age,
            course=course
        )
        messages.success(request, f'Student "{name}" has been added successfully!')
        return redirect('students:student_list')

    return render(request, 'students/add.html')

# 👉 DELETE STUDENT
@login_required(login_url='students:login')
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student_name = student.name
    student.delete()
    messages.success(request, f'Student "{student_name}" has been deleted successfully!')
    return redirect('students:student_list')

# 👉 UPDATE STUDENT
@login_required(login_url='students:login')
def update_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        student.name = request.POST['name']
        student.age = request.POST['age']
        student.course = request.POST['course']
        student.save()
        messages.success(request, f'Student "{student.name}" has been updated successfully!')
        return redirect('students:student_list')

    return render(request, 'students/update.html', {'student': student})

# 👉 SEARCH STUDENT
@login_required(login_url='students:login')
def search_student(request):
    query = request.GET.get('q', '').strip()
    if query:
        students = Student.objects.filter(name__icontains=query)
        if not students:
            messages.info(request, f'No students found matching "{query}".')
    else:
        students = Student.objects.all()
        messages.info(request, 'Showing all students.')
    return render(request, 'students/list.html', {'students': students})
