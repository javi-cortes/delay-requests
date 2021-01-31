from django.dispatch import receiver
from django.db import models
from datetime import timedelta
from django.db.models.signals import post_save


class Requests(models.Model):
    url = models.TextField()

    HTTP_VERBS = (
        ('POST', 'POST'),
        ('GET', 'GET'),
        ('HEAD', 'HEAD'),
        ('PUT', 'PUT'),
        ('DELETE', 'DELETE'),
        ('CONNECT', 'CONNECT'),
        ('OPTIONS', 'OPTIONS'),
        ('TRACE', 'TRACE'),
        ('PATCH', 'PATCH'),
    )
    http_verb = models.CharField(
        max_length=10,
        null=True,
        choices=HTTP_VERBS,
        default="GET"
    )

    state = models.CharField(max_length=10, null=True)
    datetime = models.DateTimeField(max_length=30)
    response = models.TextField(null=True)


    def save(self, *args, **kwargs):
        is_new = not self.id
        super().save(*args, **kwargs)
        if is_new:
            delay_request.apply_async(
                eta=self.datetime,
                args=(self.id, self.url, self.http_verb)
            )


from .tasks import delay_request