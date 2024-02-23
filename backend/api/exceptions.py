from django.conf import settings
from django.http import FileResponse
from django.shortcuts import render
from rest_framework.views import exception_handler


def page_not_found(exception, request):
    return render(request, 'api/404.html', status=404)