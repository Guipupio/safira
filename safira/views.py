from django.http import JsonResponse
from django.shortcuts import render

def home(request):
    return render(request,'safira/home.html')
    
def index(request):
    return render(request,'safira/index.html')