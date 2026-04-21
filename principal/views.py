from django.shortcuts import render

def home(request): # <--- Revisa que diga "home" en minúsculas
    return render(request, 'principal/index.html')
