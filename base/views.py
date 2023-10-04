from django.shortcuts import redirect, render
from .models import *
from django.contrib import messages

def receipes(request):
    queryset = Receipe.objects.all()

    if request.method == 'POST':
        data = request.POST

        receipe_name = data.get('receipe_name')
        receipe_description = data.get('receipe_description')
        receipe_image = request.FILES.get('receipe_image')

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
