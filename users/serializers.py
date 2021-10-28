from django.http import request
from rest_framework import serializers
from . models import *
from rest_framework.serializers import ModelSerializer, Serializer


class NormalSerializer(Serializer):

    data = serializers.CharField(required=True)
    
    class Meta:
        fields = ['data']



class UserRegisterSerializer(Serializer):

    tenant_id = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    profile_url = serializers.CharField(required=True)
    status = serializers.CharField(required=True)
    position = serializers.CharField(required=True)

    class Meta:
        fields = ['tenant_id', 'name', 'email', 'profile_url',
                  'status', 'position']
