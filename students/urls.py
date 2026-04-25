from django.urls import path
from . import views

app_name = "students"

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('add/', views.add_student, name='add_student'),
    path('delete/<int:id>/', views.delete_student, name='delete_student'),
    path('update/<int:id>/', views.update_student, name='update_student'),

    path('search/', views.search_student, name='search_student'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]