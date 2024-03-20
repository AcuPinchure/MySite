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
import re

# Create your views here.


def readContentHash():
    """
    read contenthash value of the main.js and vendors.js
    """
    static_path = Path(__file__).resolve().parent.parent / \
        'static' / 'twitter_bot'

    main_hash = None
    vendor_hash = None

    # List files in the directory
    files = os.listdir(static_path)

    # Regex pattern to match hash values in filenames
    pattern = r'(main|vendors)\.([a-f0-9]{20})\.js'

    # Iterate over files and extract hash values for main and vendor
    for file in files:
        match = re.match(pattern, file)
        if match:
            hash_value = match.group(2)
            file_type = match.group(1)
            if file_type == 'main':
                main_hash = hash_value
            elif file_type == 'vendors':
                vendor_hash = hash_value

    return main_hash, vendor_hash


def index(request):
    main_hash, vendor_hash = readContentHash()
    return render(request, 'twitter_bot/index.html', {
        'main_hash': main_hash,
        'vendor_hash': vendor_hash
    })


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
    main_hash, vendor_hash = readContentHash()
    return render(request, 'twitter_bot/index.html', {
        'main_hash': main_hash,
        'vendor_hash': vendor_hash
    })


def indexLogout(request):
    logout(request)
    return redirect("bot:about")


def indexLoginRequired(request):
    if not request.user.is_authenticated:
        return redirect("bot:login")
    main_hash, vendor_hash = readContentHash()
    return render(request, 'twitter_bot/index.html', {
        'main_hash': main_hash,
        'vendor_hash': vendor_hash
    })


def notFound(request):
    return render(request, 'twitter_bot/not_found.html')
