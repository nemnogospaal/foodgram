from http import HTTPStatus

from django.shortcuts import render


def page_not_found(exception, request):
    return render(request, 'api/404.html', status=HTTPStatus.NOT_FOUND)
