from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .models import Todo
from .forms import TodoForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'todo/home.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})
    
    else: 
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')

            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': "username already exists."})

        else:
            return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': "Password did not match."})
            # tell the user the passwords didn't match.


@login_required
def currenttodos(request):
    todos = Todo.objects.filter(todocreator=request.user, datecompleted__isnull=True)
    
    return render(request, 'todo/currenttodos.html', {'todos': todos})


@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, todocreator=request.user)

    if request.method == 'GET':
        form = TodoForm(instance=todo)

        return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')

        except ValueError:
            return render(request, 'todo/createtodo.html', {'todo': todo, 'form': TodoForm(), 'error': 'invalid info'})

@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, todocreator=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')


@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, todocreator=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')


@login_required
def completedtodos(request):
        todos = Todo.objects.filter(todocreator=request.user, datecompleted__isnull=False).order_by('-datecompleted')
        return render(request, 'todo/completedtodos.html', {'todos': todos})


def logoutuser(request):
    logout(request)
    return redirect('home')


def loginuser(request):
    
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})

    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])  # will give us an user object if the user is authenticated
        print(user)
        print(type(user))
        
        if user:
            login(request, user)
            return redirect('home')
        
        elif not user:
            return render(request, 'todo/loginuser.html', {'form': AuthenticationForm(), 'error': 'username and password didn\'t match'})
            


@login_required
def createtodo(request):
    
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form': TodoForm()})
    
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.todocreator = request.user
            newtodo.save()
            
            return redirect('currenttodos')
        
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form': TodoForm(), 'error': 'Bad data passed in.'})
        