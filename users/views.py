from cassandra import ProtocolVersion
from django.shortcuts import render
import uuid
from django.utils.translation import deactivate
from . models import*
import datetime, string, random
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.generics import ListCreateAPIView, ListAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework import authentication, serializers, status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView, DestroyAPIView, \
                                    ListCreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny
import json, jwt
import requests
from django.conf import settings
from . utils import *
import math, random
from django.core.mail import send_mail
from rest_framework.exceptions import APIException
from . serializers import NormalSerializer
from cassandra.cluster import Cluster


cluster = Cluster(['127.0.0.1'], control_connection_timeout=10,  port=9042)
session = cluster.connect()
print('session', session)



def homepage(request):
    print('homepage')
    return render(request,'home.html')


class TestView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = NormalSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST,
                                  "message": serializer.errors,
                                  "results":{}},
                            status= status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data['data']
        # try:
        #     data = data_decryptor(str(data))
        #     print('data',data)
        # except:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST,
        #                      "message": "Error in data decryption",
        #                      "results":{}},
        #                     status=status.HTTP_400_BAD_REQUEST)

        data = json.loads(data)
        print('data', data)
        print(type(data))
        organization_name = data.get('organization_name')
        phone_no = data.get('phone_no')
        employee_strength = data.get('employee_strength')
        domain_name = data.get('domain_name')
        country = data.get('country')
        state = data.get('state')
        city = data.get('city')

        letters = string.ascii_letters
        random_string = ''.join(random.choice(letters) for i in range(16))

        tenant_id = uuid.uuid4()
        tenant_name = organization_name + '_' + random_string

        print('organization_name', organization_name)
        print('employee_strength', employee_strength)
        print('phone_no', phone_no)
        print('domain_name', domain_name)
        print('country', country)
        print('state', state)
        print('city', city)
        print('tenant_id', tenant_id)
        print('tenant_name', tenant_name)

        session.execute("""INSERT INTO master.tenant_model
        (tenant_id, tenant_name, organization_name, phone_no, employee_strength, domain_name,
        country, state, city)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
        (tenant_id,tenant_name,organization_name, phone_no, employee_strength,
        domain_name, country, state, city))

        b = "{'class': 'SimpleStrategy', 'replication_factor': '1'}"
        session.execute(f"""CREATE KEYSPACE {tenant_name} WITH replication = {b}""")


        session.execute(f"""CREATE TABLE {tenant_name}.user_token_model (
                        user_token_id uuid PRIMARY KEY, 
                        user_id uuid, 
                        user_token text,
                        created_at timestamp,
                        created_by uuid, 
                        updated_at timestamp,
                        updated_by uuid,
                        deleted_at timestamp,
                        deleted_by uuid,
                        deleted_record boolean)""")

        session.execute(f"""CREATE TABLE {tenant_name}.user_model (
                        user_id uuid PRIMARY KEY,
                        blocked_by uuid,
                        created_at timestamp,
                        created_by uuid,
                        deleted_at timestamp,
                        deleted_by uuid,
                        deleted_record boolean,
                        device_token map<text, frozen<list<text>>>,
                        email text,
                        is_online boolean,
                        name text,
                        otp int,
                        otp_created_at timestamp,
                        position text,
                        profile_url text,
                        report_to uuid,
                        status text,
                        updated_at timestamp,
                        updated_by uuid)""")
        
        session.execute(f"""CREATE TABLE {tenant_name}.message_model (
                        message_id uuid PRIMARY KEY,
                        created_at timestamp,
                        created_by uuid,
                        delete_type text,
                        deleted_at timestamp,
                        deleted_by uuid,
                        deleted_record boolean,
                        file list<text>,
                        gif_url text,
                        group_id uuid,
                        image list<text>,
                        is_deleted boolean,
                        is_reply boolean,
                        message text,
                        read_by list<frozen<map<text, text>>>,
                        reply_data map<text, text>,
                        sender_id uuid,
                        sender_name text,
                        team_id uuid,
                        time timestamp,
                        type text,
                        updated_at timestamp,
                        updated_by uuid)""")

        session.execute(f"""CREATE TABLE {tenant_name}.group_model (
                        group_id uuid PRIMARY KEY,
                        admin_id uuid,
                        created_at timestamp,
                        created_by uuid,
                        deleted_at timestamp,
                        deleted_by uuid,
                        deleted_record boolean,
                        group_name text,
                        group_profile text,
                        group_type text,
                        is_channel boolean,
                        members list<uuid>,
                        read_by list<frozen<map<text, text>>>,
                        recent_message map<text, text>,
                        team_id uuid,
                        type text,
                        updated_at timestamp,
                        updated_by uuid)""")
                                    
        session.execute(f"""CREATE TABLE {tenant_name}.badge_model (
                        badge_id uuid PRIMARY KEY,
                        badge int,
                        created_at timestamp,
                        created_by uuid,
                        deleted_at timestamp,
                        deleted_by uuid,
                        deleted_record boolean,
                        group_id uuid,
                        updated_at timestamp,
                        updated_by uuid,
                        user_id uuid)""")
        
        session.execute(f"""CREATE TABLE {tenant_name}.team_model (
                        team_id uuid PRIMARY KEY,
                        admin_id uuid,
                        created_at timestamp,
                        created_by uuid,
                        deleted_at timestamp,
                        deleted_by uuid,
                        deleted_record boolean,
                        is_public boolean,
                        members list<uuid>,
                        profile text,
                        team_name text,
                        time timestamp,
                        updated_at timestamp,
                        updated_by uuid)""")
    
        return Response(
            data={
                "status":status.HTTP_200_OK,
                "message":"data",
                "results": {'data': 'data'}},
            status=status.HTTP_200_OK
        )