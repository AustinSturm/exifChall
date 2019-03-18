from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UploadFileForm
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import exifread
import uuid
from .models import images
from exif.settings import MEDIA_ROOT

from jose import jwt
import json

from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout

def imagePath():
    return ""


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            # need to get this to auth and redirect
            #user = authenticate(username=username, password=raw_password)
            #login(user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def signout(request):
    logout(request)
    return redirect("/")

# Create your views here.
def index(request):
    return render(request, 'base.html')

@login_required
@csrf_exempt
def upload(request):
    if request.method == 'POST':
        frm = UploadFileForm(request.POST, request.FILES)
        if frm.is_valid():
            upload = frm.save(commit=False)
            upload.user = request.user
            upload.filename = request.FILES.get("ifile")._get_name()
            upload.save()
            return redirect('/exif/{0}'.format(upload.get_upldName()))
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

@login_required
def imageView(request, **kwargs):
    form = None
    tags = "Looks like you made a mistake"
    filename = ""
    filename = kwargs.get('filename')
    try:
        with open(images.objects.get(user=request.user, ifile__endswith=filename).ifile.path, 'rb') as f:
            tags = exifread.process_file(f, details=False)
        if not tags:
            tags = {"":"There is no exif data"}
    except Exception as e:
        print(e)
    # send url to document_view function with filename
    return render(request, 'image.html', {'tags' : tags, 'filepath':'media/'+filename})

# media/filename endpoint. Redirects to nginx served files.
@login_required
def document_view(request, filename):
    document = images.objects.get(user=request.user, ifile__endswith=filename)
    response = HttpResponse()
    response["Content-Disposition"] = "attachment; filename={0}".format(document.filename)
    response['X-Accel-Redirect'] = "/protected/user-{0}/{1}".format(str(request.user.id),document.get_upldName())
    return response


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

@login_required
def admin(request, **kwargs):
    # check if token could exist (if not say not authed)
    token = request.COOKIES.get('jwtsess')

    return validateToken(request, 'adminFlag.html', 'BCTF{test}')

@login_required
def profile(request, **kwargs):
    uploads = images.objects.filter(user=request.user)

    return render(request, 'profile.html', {'uploads': uploads})
