from rest_framework import serializers
from .models import Requests
# Serializers define the API representation.


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requests
        fields = ['url', 'state', 'datetime']


 