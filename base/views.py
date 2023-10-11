from django.shortcuts import redirect, render
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/') #redirect when user is not logged in
def receipes(request):
    queryset = Receipe.objects.all()

    if request.method == 'POST':
        data = request.POST

        receipe_name = data.get('receipe_name')
        receipe_description = data.get('receipe_description')
        receipe_image = request.FILES.get('receipe_image')

        print("receipe_description:", receipe_description)  # Add this line for debugging

        Receipe.objects.create(
            receipe_name=receipe_name,
            receipe_description=receipe_description,
            receipe_image=receipe_image
        )
        messages.success(request, "Receipes added succefully!!")
        return redirect('/')

    if request.GET.get('search'):
        queryset = queryset.filter(receipe_name__icontains = request.GET.get('search'))


    context = {'receipes': queryset}
    return render(request, 'receipes.html', context)

def update_receipe(request, id):
    queryset = Receipe.objects.get(id=id)

    if request.method == 'POST':
        data = request.POST

        receipe_name = data.get('receipe_name')
        receipe_description = data.get('receipe_description')
        receipe_image = request.FILES.get('receipe_image')

        queryset.receipe_name = receipe_name
        queryset.receipe_description = receipe_description
        
        if receipe_image:
            queryset.receipe_image = receipe_image

        queryset.save() 
        messages.info(request, "Receipes updated succefully!!")
        return redirect("/")
    
    context = {'receipe': queryset}
    return render(request, 'update_receipe.html', context)

def delete_receipe(request, id):
    queryset = Receipe.objects.get(id=id) 
    queryset.delete()
    messages.warning(request, "Receipes deleted succefully!!")
    return redirect('/')


def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
    
        if not User.objects.filter(username = username).exists():
            messages.alert(request, 'Invalid username')
            return redirect("/login/")
        
        user = authenticate(username = username, password = password)

        if user is None:
            messages.warning(request, "Invalid credientied")
            return redirect("/login/")
        else: 
            login(request, user)   
            return redirect("/")
    
    return render(request, 'login.html') 


def logout_page(request):
    logout(request) 
    return redirect("/login/")

def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # checking user is present in db

        user = User.objects.filter(username = username)

        if user.exists():
            messages.warning(request, 'username already taken!')
            return redirect('/register')

        # insert user into db

        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username,
        )

        # pass convert into encrypted password 
        
        user.set_password(password)
        user.save()

        messages.success(request, 'Account created successfully!')
        return redirect("/login")

    return render(request, 'register.html') 