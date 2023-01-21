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

# def LogIn(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#         else:
#             print('ERROORRRRRRR')
#         return redirect('/')
#     else:
#         print('kek')
#         return render(request, 'login.html')
#
#
def LogOut(request):
    logout(request)
    return redirect('/')





# def post_detail(request, slug):
#     post = get_object_or_404(Post, slug=slug)
#     if request.user.is_active:
#         if request.method == "POST":
#             comment_form = CommentForm(request.POST)
#
#             if comment_form.is_valid():
#                 comment = comment_form.save(commit=False)
#                 comment.content_object = post
#                 comment.creator = request.user
#                 comment.save()
#                 logger.info("Created comment on Post %d for user %s", post.pk, request.user)
#                 return redirect(request.path_info)
#         else:
#             comment_form = CommentForm()
#     else:
#         comment_form = None
#     return render(request, "blog/post-detail.html", {"post": post, "comment_form": comment_form})



def LogIn(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            username = login_form.data.get('username')
            password = login_form.data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, message='Done')
                return redirect('/')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')
    login_form = AuthenticationForm()
    return render(request, 'login.html', context={'login_form': login_form})


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