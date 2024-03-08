from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
from django.contrib import auth
from django.contrib.auth.decorators import login_required


@login_required(login_url='/signin')
def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, 'User created successfully')
                #log user in and send them to settings page
                #create profile for user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model,id_user=user_model.id)
                new_profile.save()
                return redirect('signup')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')
    else:
        return render(request, 'signup.html')

def signin(request):
    
    
    if request.method == 'POST':
        username = request.POST['username']
        password= request.POST['password']
        user= auth.authenticate(username=username, password=password)

        if user is None:
            messages.error(request, 'No such user exists. Please sign up.')
            return redirect('signin')
        else:
            if user.check_password(password):
                return redirect('/')
            else:
                messages.error(request, 'Incorrect username or password')
                return redirect('signin')
            
    else:
        return render(request, 'signin.html')

def logout(request):
    auth.logout(request)
    return redirect('signin')