from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import todo

@login_required
def home(request):
    if request.method == "POST":
        task = request.POST.get('task')
        
        new_todo=todo(user=request.user, todo_name=task)
        new_todo.save()

    all_todos = todo.objects.filter(user=request.user)

    contexts={
        'todos': all_todos
    }
    return render(request, 'todoapp/todo.html', contexts)

def register(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    if request.method == "POST":
        password = request.POST.get('password')
        email = request.POST.get('email')

        username = request.POST.get('username')
        if len(password) <6:
            messages.error(request, "Password must be greater than 6 characters")
            return redirect('register-page')

        get_existing_username = User.objects.filter(username=username)
        if get_existing_username:
            messages.error(request, "User already exists!! Try another one.")
            return redirect('register-page')
        
        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.save()
        messages.success(request, 'User successfully created')
        return redirect('login-page')
    return render(request, 'todoapp/register.html', {})

def user_login(request):
    if request.method == "POST":
        password = request.POST.get('pass')
        username = request.POST.get('uname')

        validate_user = authenticate(username=username, password=password)
        if validate_user is not None:
            login(request, validate_user)
            return redirect('home-page')
        else:
            messages.error(request, "User not exists!!")
            return redirect('login-page')

    return render(request, 'todoapp/login.html', {})

def LogoutView(request):
    logout(request)
    return redirect('login-page')

@login_required
def DeleteTask(request, name):
    get_todo = todo.objects.get(user=request.user, todo_name=name)
    get_todo.delete()
    return redirect('home-page')

@login_required
def Update(request, name):
    get_todo = todo.objects.get(user=request.user, todo_name=name)
    get_todo.status = True
    get_todo.save()
    return redirect('home-page')