from django.shortcuts import render
import openai, os
from dotenv import load_dotenv

load_dotenv()
# Create your views here.

def sensei(request):
    return render(request,'sensei_base.html')