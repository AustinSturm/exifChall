from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UploadFileForm
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import exifread
import uuid

from jose import jwt
import json

from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def signout(request):
    logout(request)
    return redirect("/")

# Create your views here.
def index(request):
    print(request.user)
    return render(request, 'base.html')

@login_required
@csrf_exempt
def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        print(request.FILES)
        file_handle(request)
        return redirect('/img/' + request.FILES.get("myfile")._get_name())
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

# cud add flag here for stego
def file_handle(request):
    try:
        path = 'front/media/'+str(request.user.id) + "/"+request.FILES.get("myfile")._get_name()
        with open(path,'wb+') as dest:
            for chunk in request.FILES.get("myfile").chunks():
                dest.write(chunk)
    except Exception as e:
        print(e)


def imageView(request, **kwargs):
    form = None
    filename = kwargs.get('filename')
    try:
        with open('front/media/'+filename, 'rb') as f:
            tags = exifread.process_file(f, details=False)
        if not tags:
            tags = {"":"There is no exif data"}
    except Exception as e:
        print(e)
    return render(request, 'image.html', {'tags' : tags, 'filename':filename})


def validateToken(request, template, flag):
    token = request.COOKIES.get('jwtsess')

    if token:
        # check if token is valid (if not state invalid token)
        try:
            secret = "test"
            decoded = jwt.decode(token, secret)
        except Exception as e:
            print(e)
            return render(request, template, {'output': e})

        # cant be bothered to implement this legit so hardcoded cases
        try:
            if decoded['user'].lower() == 'therock':
                if decoded['role'].lower() == 'admin':
                    return render(request, template, {'output': flag})
        except:
            return render(request, template, {'output': "Not valid user/role"})

    return render(request, template, {'output': "Not Logged In"})

def admin(request, **kwargs):
    # check if token could exist (if not say not authed)
    token = request.COOKIES.get('jwtsess')

    return validateToken(request, 'adminFlag.html', 'BCTF{test}')

def profile(request, **kwargs):
    # check if token could exist (if not say not authed)
    token = request.COOKIES.get('jwtsess')

    return validateToken(request, 'profile.html', 'BCTF{test2}')
