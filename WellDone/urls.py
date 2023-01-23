"""WellDone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from task import views, forms

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.TaskListView, name='home'),
    path('task/<int:id>', views.TaskDetailView, name='task-detail'),
    path('delete/<int:id>', views.DeleteTask, name='delete-task'),
    path('logout/', views.LogOut, name='logout'),
    path('login/', views.LoginView, name='login'),
    path('register/', views.Registration, name='register'),
    path('solve/<int:id>', views.SolveTask, name='solve-task'),
    path('unsolve/<int:id>', views.UnsolveTask, name='unsolve-task'),
    path('solved-tasks/', views.SolveTaskListView, name='solved-tasks-list'),
    path('edit/<int:id>', views.EditTaskView, name='edit-task'),
    path('user/<int:id>', views.UserDetailView, name='user-detail'),

]
