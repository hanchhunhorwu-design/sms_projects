from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Student

# 👉 LOGIN
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('students:student_list')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'students/login.html', {})

# 👉 LOGOUT
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('students:login')

# 👉 SHOW LIST
def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/list.html', {'students': students})

# 👉 ADD STUDENT
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
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student_name = student.name
    student.delete()
    messages.success(request, f'Student "{student_name}" has been deleted successfully!')
    return redirect('students:student_list')

# 👉 UPDATE STUDENT
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