from rest_framework.views import exception_handler
from rest_framework import viewsets
from .serializers import RequestSerializer
from .models import Requests


class RequestViewSet(viewsets.ModelViewSet):
    queryset = Requests.objects.all()
    serializer_class = RequestSerializer


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    print(response.__dict__)

    return response

