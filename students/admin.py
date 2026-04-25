
from django.shortcuts import render, redirect
from .models import Student

def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/list.html', {'students': students})

def add_student(request):
    if request.method == "POST":
        name = request.POST['name']
        age = request.POST['age']
        course = request.POST['course']
        Student.objects.create(name=name, age=age, course=course)
        return redirect('student_list')
    return render(request, 'students/add.html')

def delete_student(request, id):
    student = Student.objects.get(id=id)
    student.delete()
    return redirect('student_list')
