from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url="/login/")
def receipes(request):
    
    # if not request.user.is_authenticated:
    #     return redirect("/login/")
    
    if request.method == "POST":
        data = request.POST    
  
        receipe_name = data.get("receipe_name")
        receipe_description = data.get("receipe_description")
        receipe_image = request.FILES.get('receipe_image')
        
        Receipe.objects.create(
            receipe_image = receipe_image,
            receipe_description = receipe_description,
            receipe_name = receipe_name
        )
        
        return(redirect("/"))
        
   
    querryset = Receipe.objects.all()
    
    
    if request.GET.get('search'):
        print(request.GET.get('search'))
        querryset = querryset.filter(receipe_name__icontains = request.GET.get('search'))
        
    context = {'receipes':querryset}
        
    return render(request,"receipes.html",context)

def delete_receipe(request,id):
    querryset = Receipe.objects.get(id=id)
    querryset.delete()
    # print(id)
    return redirect("/")

@login_required(login_url="/login/")
def update_receipes(request,id):
    querryset = Receipe.objects.get(id = id)
    context = {"receipe":querryset}
    
    if request.method == "POST":
        data = request.POST
        
        receipe_name = data.get("receipe_name")
        receipe_description = data.get("receipe_description")
        receipe_image = request.FILES.get('receipe_image')
        
        querryset.receipe_name = receipe_name
        querryset.receipe_description = receipe_description
        if receipe_image:
            querryset.receipe_image = receipe_image 
        
        querryset.save()  
        return redirect('/')   
    
    return render(request,'update_receipe.html',context)


def login_Page(request):
    
    if request.method == "POST":
        username = request.POST.get('user_name')
        password = request.POST.get('password')
        
        if not User.objects.filter(username = username).exists():
            messages.warning(request,"Invalid Username!")
            return redirect('/login/')
        
        user = authenticate(username = username,password = password)
        
        if user is None:
            messages.warning(request,"Invalid Password!")
            return redirect("/login/")
        
        else:
            login(request,user)
            return redirect("/")
    
    return render(request,"login.html")

def logout_Page(request):
    
    logout(request)
    
    return redirect("/login/")

def register_Page(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')  # Correct field name
        last_name = request.POST.get('last_name')    # Correct field name
        username = request.POST.get('user_name')
        password = request.POST.get('password')
        
        checkuser = User.objects.filter(username = username)
        
        if checkuser.exists():
            print("User already exist !")
            messages.warning(request,"Username already taken! use anathor")
            return redirect("/register/")
        
        user = User.objects.create(
            first_name=first_name,  
            last_name=last_name,    
            username=username,
        )
        user.set_password(password)  # Encrypt the password
        user.save()
        messages.success(request,"User register successfully")
        
        return redirect('/login/')
    
    return render(request, "register.html")