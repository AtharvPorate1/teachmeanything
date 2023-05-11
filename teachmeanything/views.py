from django.shortcuts import render, redirect

def homepage(request):
    return render(request,'landing_page.html')