from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    # return HttpResponse("Hello World. you are at  home")
    return render(request,'website/index.html')

def about(request):
    # return HttpResponse("Hello World. you are at  about")
    return render(request,'website/aboutus.html')

def contact(request):
    # return HttpResponse("Hello World. you are at  contact")
    return render(request,'website/contact.html')