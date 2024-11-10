from django.shortcuts import render,redirect, get_object_or_404
from django.views.decorators.clickjacking import xframe_options_exempt
from django.template import loader, Context
from django.http import HttpResponse, HttpResponseRedirect
from copy import copy
from .forms import FileUploadForm
from .utils import handle_uploaded_file
from .models import UploadedFile
from django.views.decorators.csrf import csrf_exempt
import os




@xframe_options_exempt
def home_view(request):
    # You can pass a dynamic message here, for example, based on some logic or request parameters.
    template = loader.get_template('main.html')
    return HttpResponse(template.render())
# Create your views here.



# def upload_view(request):
#     if request.method == "POST":
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             handle_uploaded_file(request.FILES["file"])
#             return HttpResponseRedirect("/success/url/")
#     else:
#         form = UploadFileForm()
#     return render(request, "upload.html", {"form": form})

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
            uploaded_file = form.save()

            # Optionally save the file locally (if needed)
            save_file_locally(uploaded_file.file)

            # Redirect to a success page
            return redirect('success')
    else:
        # Render an empty form for uploading a new file
        form = FileUploadForm()

    # Render the file upload form
    return render(request, 'upload_file.html', {'form': form})


def save_file_locally(file_field):
    """
    Save the uploaded file to a local directory.
    - file_field: FileField or the uploaded file object to be saved locally.
    """
    import os

    # Define the local directory path where files will be saved
    local_directory = 'local_directory/'
    os.makedirs(local_directory, exist_ok=True)  # Create the directory if it doesn't exist

    # Construct the local file path
    local_file_path = os.path.join(local_directory, os.path.basename(file_field.name))

    # Save the file content locally
    with open(local_file_path, 'wb') as local_file:
        for chunk in file_field.chunks():
            local_file.write(chunk)




def success(request):
    template = loader.get_template('success.html')
    return HttpResponse(template.render())



