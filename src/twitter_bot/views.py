from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from pathlib import Path
import os
from django.conf import settings

# models and query
from .models import Seiyuu, WeeklyStats, Tweet, UserAccount, Followers
from django.db.models import Avg, Count, Sum

# rest framework
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# time utils
from django.utils import timezone
from datetime import datetime, timedelta
import pytz

# Create your views here.
root_path = Path(__file__).resolve().parent.parent.parent


def index(request):
    return render(request, 'twitter_bot/index.html')


def indexLogin(request):
    if request.user.is_authenticated:
        return redirect("bot:config")
    if request.method == "POST":
        post = request.POST
        if post.get("username") and post.get("password"):
            user = authenticate(username=post.get(
                "username"), password=post.get("password"))
            if user:
                login(request, user)
                return redirect("bot:config")
    return render(request, 'twitter_bot/index.html')


def indexLogout(request):
    logout(request)
    return redirect("bot:about")


def indexLoginRequired(request):
    if not request.user.is_authenticated:
        return redirect("bot:login")
    return render(request, 'twitter_bot/index.html')


def notFound(request):
    return render(request, 'twitter_bot/not_found.html')
