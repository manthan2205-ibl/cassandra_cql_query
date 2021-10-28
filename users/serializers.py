from django.http import request
from rest_framework import serializers
from . models import *
from rest_framework.serializers import ModelSerializer, Serializer


class NormalSerializer(Serializer):

    data = serializers.CharField(required=True)
    
    class Meta:
        fields = ['data']
