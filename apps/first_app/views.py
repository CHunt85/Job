from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):

    return render(request,'first_app/index.html')

def login_fun(request):
    errors = User.objects.login_manager(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['email'])
        request.session['user_firstname']= user.first_name
        request.session['user_lastname']= user.last_name
        request.session['user_email']= user.email        
        request.session['user']= user.id
    return redirect ('/dashboard')

def create(request):
    errors = User.objects.basic_validator(request.POST)
    hash_pass = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    user = User.objects.create( first_name= request.POST['first_name'],last_name= request.POST['last_name'],email= request.POST['email'], password= hash_pass )
    user = User.objects.get(email=request.POST['email'])
    request.session['user_firstname']= user.first_name
    request.session['user_lastname']= user.last_name
    request.session['user_email']= user.email
    request.session['user']= user.id
    return redirect('/dashboard')

def dashboard(request):
    if "user_email" not in request.session:
        return redirect('/')
    else:
        context = {
            'users_o': User.objects.get(id = request.session['user']),
            'message': Job.objects.all(),
        }
    return render (request, 'first_app/dashboard.html', context)

def new(request):
    context = {
            'users_o': User.objects.get(id=request.session['user']),
     }
    if "user_email" not in request.session:
            return redirect('/')
    else:

        return render (request, 'first_app/new.html',context, {'users': User.objects.get(email = request.session['user_email'])})

def add_fun(request):
    errors = Job.objects.job_manager(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/new')
    y = User.objects.get(email= request.session['user_email'])
    print (request.POST)
    x = Job.objects.create( job= y ,title = request.POST['content1'], desc= request.POST['content2'], area= request.POST['content3'])
    y.work.add(x)
    return redirect('/dashboard')

def edit(request):
    context = {
            'users_o': User.objects.get(id=request.session['user']),
     }
    if "user_email" not in request.session:
        return redirect('/')
    else:
        return render(request,'first_app/edit.html',context)

def edit_fun(request):
    errors = Job.objects.job_manager(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/edit')
    else:
        job= Job.objects.get(id = request.session['user'])
        job.job = request.POST['job']
        job.desc = request.POST['desc']
        job.area = request.POST['area']
        job.save()
    return redirect('/dashboard')

def info(request, id):
    if "user_email" not in request.session:
        return redirect('/')
    else:
        context = {
            'users_o': User.objects.get(id = request.session['user']),
            'message': Job.objects.all(),
        }
        return render(request,'first_app/info.html', context)

def destroy(request):
    x= Job.objects.get(id=request.POST['product'])
    x.delete()
    return redirect('/dashboard')

def logout(request):
    request.session.clear()
    return redirect ('/')