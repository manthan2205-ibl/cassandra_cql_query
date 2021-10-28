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
from . authentication import *
import math, random
from django.core.mail import send_mail
from rest_framework.exceptions import APIException
from . serializers import *
from cassandra.cluster import Cluster


# cluster = Cluster(['127.0.0.1'], control_connection_timeout=10,  port=9042)
cluster = Cluster()
session = cluster.connect()
print('session', session)



def homepage(request):
    print('homepage')
    return render(request,'home.html')


class OnbordView(GenericAPIView):
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


        tenant_dic = {}
        tenant_dic['tenant_id']=tenant_id
        tenant_dic['tenant_name']=tenant_name
        tenant_dic['organization_name']=organization_name
        tenant_dic['phone_no']=phone_no
        tenant_dic['employee_strength']=employee_strength
        tenant_dic['domain_name']=domain_name
        tenant_dic['country']=country
        tenant_dic['state']=state
        tenant_dic['city']=city

        


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
                "results": {'data': tenant_dic}},
            status=status.HTTP_200_OK
        )




class UserRegisterView(GenericAPIView):
    permission_classes = [AllowAny]
    # queryset = UserModel.objects.all()
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        
        serializer = UserRegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST,
                                  "message": serializer.errors,
                                  "results":{}},
                            status=status.HTTP_400_BAD_REQUEST)

        tenant_id = serializer.validated_data['tenant_id']
        tenant_id = uuid.UUID(tenant_id)
        name = serializer.validated_data['name']
        email = serializer.validated_data['email']
        profile_url = serializer.validated_data['profile_url']
        statuss = serializer.validated_data['status']
        position = serializer.validated_data['position']

        device_token = {"mobile":[], "desktop":[],"web":[]}


        result = session.execute("""
                        SELECT * FROM master.tenant_model WHERE tenant_id = %s
                        """,
                        [tenant_id]).one()

        print('result', result)
        tenant_name = result.tenant_name
        tenant_name = tenant_name.lower()
        print('tenant_name', tenant_name)


        check_email = session.execute(f"""
                        SELECT * FROM {tenant_name}.user_model WHERE email = %s ALLOW FILTERING """,
                        [email]).one()

        print('check_email', check_email)

        if check_email:
            return Response(data={"status": status.HTTP_400_BAD_REQUEST,
                                  "message": "User Email Already Registered",
                                  "results":{}},
                            status=status.HTTP_400_BAD_REQUEST)



        user_id = uuid.uuid4()
        # a = f'INSERT INTO {tenant_name}.user_model'
        # print(a)
        session.execute(f"""INSERT INTO {tenant_name}.user_model
        (user_id, name, email, profile_url, status, position, device_token)
        VALUES (%s, %s, %s, %s, %s, %s, %s)""",
        (user_id, name, email, profile_url, statuss, position, device_token))
           
        return Response(data={"status": status.HTTP_201_CREATED,
                                "message": "User Registered",
                                "results": { 'data' : serializer.data} },
                        status=status.HTTP_201_CREATED)



class UserLoginView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = NormalSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST,
                                  "message": serializer.errors,
                                  "results":{}},
                            status= status.HTTP_400_BAD_REQUEST)

        # email = serializer.validated_data['email']
        data = serializer.validated_data['data']
        try:
            # email = data_decryptor(email)
            # print('email',email)
            data = data_decryptor(str(data))
            print('data',data)
        except:
            return Response(data={"status": status.HTTP_400_BAD_REQUEST,
                             "message": "Error in data decryption",
                             "results":{}},
                            status=status.HTTP_400_BAD_REQUEST)

        data = json.loads(data)
        print('data', data)
        print(type(data))
        email = data.get('email')
        
        if not UserModel.objects.filter(email=email,deleted_record=False).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST,
                             "message": "The email address is not register, Please register first",
                             "results":{}},
                            status=status.HTTP_400_BAD_REQUEST)

        if UserModel.objects.filter(email=email,deleted_record=False).exists():
            user = UserModel.objects.filter(email=email,deleted_record=False).first()

            # deleted_by = user.deleted_by
            # if deleted_by == None:
            #     print('deleted_by', deleted_by)

            digits = "0123456789"
            OTP = ""
            for i in range(6) :
                OTP += digits[math.floor(random.random() * 10)]

            print('OTP', OTP)

            user.otp = int(OTP)
            user.otp_created_at = datetime.datetime.utcnow()
            user.save()

            try:
                message = "Your OTP  for verify email \n" \
                            "OTP :-  {0}".format(OTP)
                send_mail('OTP verification', message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
            except:
                return Response(data={"status": status.HTTP_400_BAD_REQUEST,
                                 "message": "Email send is failed, Please enter valid email.",
                                 "results":{}},
                                status=status.HTTP_400_BAD_REQUEST)
 

            return Response(data={"status": status.HTTP_200_OK,
                                  "message": "OTP has been sent to your mail, Please check email.",
                             "results": {}},
                            status= status.HTTP_200_OK)
        else:
            return Response(data={"status": status.HTTP_400_BAD_REQUEST,
                 "message": "The email address is not register, Please register first",
                 "results":{}},
                            status=status.HTTP_400_BAD_REQUEST)





class OTPVerifyView(GenericAPIView):
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
        try:
            data = data_decryptor(data)
            print('data',data)
        except:
            return Response(data={"status": status.HTTP_400_BAD_REQUEST,
                             "message": "Error in data decryption",
                             "results":{}},
                            status=status.HTTP_400_BAD_REQUEST)

        data = json.loads(data)
        print('data', data)
        print(type(data))
        email = data.get('email')
        token_type = data.get('token_type')
        device_token = data.get('device_token')
        otp = data.get('otp')

        

        if not UserModel.objects.filter(email=email,deleted_record=False).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST,
                             "message": "The email address you entered is invalid, Please recheck.",
                             "results":{}},
                            status=status.HTTP_400_BAD_REQUEST)

        if UserModel.objects.filter(email=email,deleted_record=False).exists():
            user = UserModel.objects.filter(email=email,deleted_record=False).first()

            
            database_OTP = user.otp 
            otp_time = user.otp_created_at
            current_time = datetime.datetime.utcnow()

            diffrence_time = current_time - otp_time
            print('diffrence_time', diffrence_time)
            seconds = diffrence_time.seconds
            print('seconds', seconds)
            

            if not int(otp) == int(database_OTP):
                return Response(data={"status": status.HTTP_400_BAD_REQUEST,
                                        "message": "OTP is wrong, Please enter valid OTP.",
                                        "results":{}},
                            status=status.HTTP_400_BAD_REQUEST)
            
            # if seconds > 120:
            #     return Response(data={"status": status.HTTP_400_BAD_REQUEST,
            #                             "message": "OTP is expire, Please send again.",
            #                             "results":{}},
            #                 status=status.HTTP_400_BAD_REQUEST)

            
            deviceToken = user.deviceToken    
            token_type_list = deviceToken[str(token_type)] 
            token_type_list.append(str(device_token))
            deviceToken[str(token_type)] = token_type_list
            user.deviceToken = deviceToken   
            user.save() 

            print('deviceToken', deviceToken)

            # token
            letters = string.ascii_letters
            random_string = ''.join(random.choice(letters) for i in range(15))
            payload = {'user_id': str(user.user_id), 'email': email, 'random_string': random_string }
            encoded_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

            encoded_token= encoded_token.decode("utf-8") 
            print('encoded_token', str(encoded_token))

            UserTokenModel.objects.create(user_id=user.user_id, token=encoded_token)
            serializer = UserRegisterSerializer(user)
            data = {
            'id': str(user.user_id),
            'token': encoded_token,
            'user_data':serializer.data}
            data = json.dumps(data)
            return Response(data={"status": status.HTTP_200_OK,
                                "message": "User successfully login, Token Generated.",
                            # "results": {'data':  data } },
                            "results": {'data':  data_encryptor(str(data)) } },
                            status= status.HTTP_200_OK)
        else:
            return Response(data={"status": status.HTTP_400_BAD_REQUEST,
                 "message": "The email address you entered is invalid. Please try again.",
                 "results":[]},
                            status=status.HTTP_400_BAD_REQUEST)

        

class LogoutView(GenericAPIView):
    permission_classes = [AllowAny]
    # authentication_classes = [MyOwnTokenAuthentication]
    serializer_class = NormalSerializer

    def post(self, request, *args, **kwargs):
        try:
            token = Authenticate(self, request)
            # print('token', token)
            user = request.user
            serializer = self.get_serializer(data=request.data)

            if not serializer.is_valid():
                return Response(data={"status": status.HTTP_400_BAD_REQUEST,
                                    "message": serializer.errors,
                                    "results":{}},
                                status= status.HTTP_400_BAD_REQUEST)

            data = serializer.validated_data['data']
            try:
                data = data_decryptor(data)
                print('data',data)
            except:
                return Response(data={"status": status.HTTP_400_BAD_REQUEST,
                                    "message": "Error in data decryption",
                                    "results":{}},
                                status=status.HTTP_400_BAD_REQUEST)

            data = json.loads(data)
            print('data', data)
            print(type(data))
            token_type = data.get('token_type')
            device_token = data.get('device_token')


            deviceToken = user.deviceToken    
            token_type_list = deviceToken[str(token_type)] 
            token_type_list.remove(str(device_token))
            # token_type_list.clear() 
            deviceToken[str(token_type)] = token_type_list
            user.deviceToken = deviceToken   
            user.save()
            try:
                token= token.decode("utf-8") 
                user_token = UserTokenModel.objects.get(user_id=request.user.user_id, 
                                        token=token, deleted_record=False)
                print('user_token', user_token)
                user_token.deleted_record = True
                user_token.deleted_at = datetime.datetime.utcnow()
                user_token.deleted_by = request.user.user_id
                user_token.save()
            except:
                return Response(data={"status": status.HTTP_400_BAD_REQUEST,
                                      "message": 'Already Logged Out.',
                                      "results":{}},
                                status=status.HTTP_400_BAD_REQUEST)
            
            

            return Response(data={"status": status.HTTP_200_OK,
                                  "message": "User Logged Out.",
                                  "results":{}},
                            status=status.HTTP_200_OK)
        except:
            return Response(data={"status":status.HTTP_400_BAD_REQUEST,
                                  "message":'Already Logged Out.',
                                  "results":{}},
                            status=status.HTTP_400_BAD_REQUEST)