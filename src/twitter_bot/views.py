from django.shortcuts import render, redirect
from django.http import HttpResponse
from pathlib import Path
import os

# Create your views here.
root_path = Path(__file__).resolve().parent.parent.parent

def about(request):
    return render(request,'twitter_bot/about.html')

def log(request):
    log_list = os.listdir(os.path.join(root_path,"crontabLog"))
    
    return render(request, 'twitter_bot/log.html', {
        'log_list': log_list
    })

def log_content(request, log_name):
    with open(os.path.join(root_path,"crontabLog",log_name),"r") as log_in:
        log_content = log_in.readlines()
    
    return render(request, 'twitter_bot/log_content.html', {
        'log_name': log_name,
        'log_content': log_content
    })

def stats(request, name):
    return render(request, f'twitter_bot/stats_{name}.html')