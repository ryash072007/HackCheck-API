import os
from django.conf import settings
from django.views.static import serve
from django.shortcuts import render

def custom_media_serve(request, path):
    # Construct the absolute file path
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    
    # Check if the file exists
    if os.path.exists(file_path) and os.path.isfile(file_path):
        # File exists, serve it using Django's serve view
        return serve(request, path, document_root=settings.MEDIA_ROOT)
    else:
        # File doesn't exist, render custom 404 template
        return render(request, '404.html', status=404)