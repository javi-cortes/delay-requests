from __future__ import absolute_import, unicode_literals

from core.celery import app

from .models import Requests as RequestsModel

import requests

@app.task
def delay_request(request_id, url, method):
    try:
        request_instance = RequestsModel.objects.get(id=request_id)
    except RequestsModel.DoesNotExists:
        return

    print(f"executing {method.lower()} to {url}")
    
    response = getattr(requests, method.lower(), lambda url: None)(url)
    request_instance.state = response.status_code
    request_instance.response = response.content
    request_instance.save()
