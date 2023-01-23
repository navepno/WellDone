from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from task.models import Task, Tag
from task.forms import *


def TaskListView(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(creator=request.user, solved_status=False).order_by('-created_at')
        tags = Tag.objects.all()
        solved_tasks = Task.objects.filter(creator=request.user, solved_status=True).order_by('-modified_at')[:5]
        if request.method == 'POST':
            task_form = TaskForm(request.POST)

            if task_form.is_valid():
                task = task_form.save(commit=False)
                task.creator = request.user
                task.save()

            return redirect(request.path_info)
        else:
            task_form = TaskForm()

        context = {
            'tasks': tasks,
            'tags': tags,
            'task_form': task_form,
            'solved_tasks': solved_tasks,
        }

        return render(request, 'task/task-list-test.html', context=context)
    else:
        tasks = Task.objects.filter(creator=1)
        tags = Tag.objects.all()
        solved_tasks = Task.objects.filter(creator=1, solved_status=True).order_by('-modified_at')[:5]

        context = {
            'tasks': tasks,
            'tags': tags,
            'solved_tasks': solved_tasks,
            # 'task_form': task_form,
        }

        return render(request, 'task/task-list-test.html', context=context)


def TaskDetailView(request, id):
    if request.user.is_authenticated:
        task = get_object_or_404(Task, id=id)
        context = {
            'task': task
        }
        return render(request, 'task/task-detail.html', context=context)
    else:
        return redirect('/')


def DeleteTask(request, id):
    if request.user.is_authenticated:
        task = get_object_or_404(Task, id=id)
        task.delete()
        return redirect('/')
    else:
        return redirect('/')


def EditTaskView(request, id):
    if request.user.is_authenticated:
        task = get_object_or_404(Task, id=id)
        if request.method == "POST":
            edit_form = TaskForm(request.POST, instance=task)
            if edit_form.is_valid():
                task = edit_form.save(commit=False)
                task.save()
        else:
            edit_form = TaskForm(instance=task)
            context = {
                'edit_form': edit_form,
                'task': task,
            }
            return render(request, 'task/edit-task.html', context=context)

        return redirect('/')
    else:
        return redirect('/')

    # return render(request, 'task/task-list.html', {'formset': test})


def SolveTask(request, id):
    if request.user.is_authenticated:
        task = get_object_or_404(Task, id=id)
        task.solved_status = True
        task.save()

        return redirect('/')
    else:
        return redirect('/')


def UnsolveTask(request, id):
    if request.user.is_authenticated:
        task = get_object_or_404(Task, id=id)
        task.solved_status = False
        task.save()

        return redirect('/')
    else:
        return redirect('/')


def SolveTaskListView(request):
    solved_tasks = Task.objects.filter(creator=request.user, solved_status=True).order_by('-modified_at')
    context = {
        'solved_tasks': solved_tasks,
    }
    return render(request, 'task/solved-tasks-list.html', context=context)


def LogOut(request):
    logout(request)
    return redirect('/')


def Registration(request):
    if request.method == 'POST':
        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():
            user = registration_form.save()
            login(request, user)
            messages.success(request, 'Correct registration')
            return redirect('/')
        else:
            messages.error(request, 'Something gone wrong')
    registration_form = RegistrationForm()
    return render(request, 'registration.html', context={'registration_form': registration_form})


def LoginView(request):
    message = ''
    if request.method == 'POST':
        login_form = UserLoginForm(request, data=request.POST)
        if login_form.is_valid():
            username = login_form.data.get('username')
            password = login_form.data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, message='Done')
                return redirect('/')
            else:
                message = 'Invalid username or password'
                messages.error(request, 'Invalid username or password')
        else:
            message = 'Invalid username or password'
            messages.error(request, 'Invalid username or password')
    login_form = UserLoginForm()

    return render(request, 'login.html', context={'login_form': login_form, 'error_message': message})


def UserDetailView(request, id):
    tasks = Task.objects.filter(creator=request.user)
    context = {
        'tasks': tasks,
    }
    return render(request, 'task/user-detail.html', context=context)