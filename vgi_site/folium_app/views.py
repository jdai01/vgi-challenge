from django.conf import settings
from django.shortcuts import render,redirect, get_object_or_404
from django.views.decorators.clickjacking import xframe_options_exempt
from django.template import loader, Context
from django.http import HttpResponse, HttpResponseRedirect
from copy import copy
from .forms import FileUploadForm
from .models import UploadedFile
from django.views.decorators.csrf import csrf_exempt
from .map_generation import map_generation
import os

upload_path = os.path.join(settings.BASE_DIR,"uploads","received.xml")

@xframe_options_exempt
def home_view(request):
    # You can pass a dynamic message here, for example, based on some logic or request parameters.
    template = loader.get_template('main.html')
    return HttpResponse(template.render())
# Create your views here.

@csrf_exempt
def upload_file(request):
    """
    Handle uploading a new file.
    - Render a form to upload a file.
    - Save the file to the database when submitted.
    """
    if request.method == 'POST':
        # Bind the form with POST data and uploaded file
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the file to the database
            # uploaded_file = form.save()

            # Optionally save the file locally (if needed)
            handle_uploaded_file(request.FILES["file"])

            # Redirect to a success page
            return redirect('success')
    else:
        # Render an empty form for uploading a new file
        form = FileUploadForm()

    # Render the file upload form
    return render(request, 'upload_file.html', {'form': form})

def handle_uploaded_file(f):
    with open(upload_path, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def success(request):
    template = loader.get_template('success.html')
    return HttpResponse(template.render())

def default_map(request):
    default_map_check = os.path.exists(os.path.join(settings.BASE_DIR,"folium_app","templates", "default_map.html"))
    if default_map_check:
        template = loader.get_template('default_map.html')
        print("template loaded!")
    else:
        map_generation.create_default_map()
        template = loader.get_template('default_map.html')
    return HttpResponse(template.render())

def dynamic_map_generation(request):

    map_generation.create_map(xml_filepath=upload_path)
    template = loader.get_template('map.html')
    return HttpResponse(template.render())


