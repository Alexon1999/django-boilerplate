import logging

from django.http import HttpResponse

logger = logging.getLogger("django")

# Create your views here.


def index(request):
    return HttpResponse("Hello World!")
