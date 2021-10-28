from rest_framework import status, exceptions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from .models import *
import jwt, json
from django.conf import settings


class MyOwnTokenAuthentication(TokenAuthentication):

    # model = UserModel

    def get_model(self):
        return UserModel

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != b'token':
            return None

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header'
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1]
            if token=="null":
                msg = 'Null token not allowed'
                raise exceptions.AuthenticationFailed(msg)
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, token):
        model = self.get_model()
        try:
            payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            email = payload['email']
            # print(user_id)
            # print(email)
            try:
                try:
                    user = UserModel.objects.get(user_id=user_id, email=email, deleted_record=False)
                    # print(user)
                except:
                    msg = {"status": status.HTTP_404_NOT_FOUND, "message": "User Not Found", "results":{}}
                    raise exceptions.AuthenticationFailed(msg)
                try:
                    encoded_token= token.decode("utf-8") 
                    user_token = UserTokenModel.objects.get(user_id=user.user_id, 
                                            token=encoded_token, deleted_record=False)
                except:
                    msg = {"status": status.HTTP_404_NOT_FOUND, "message": "Token Not Found", "results":{}}
                    raise exceptions.AuthenticationFailed(msg)

                if not str(encoded_token) == str(user_token.token):
                    msg = {"status": status.HTTP_401_UNAUTHORIZED, "message": "Token Missmatch", "results":{}}
                    raise exceptions.AuthenticationFailed(msg)

            except UserModel.DoesNotExist:
                msg = {"status" :status.HTTP_404_NOT_FOUND, "message": "User Not Found", "results":{}}
                raise exceptions.AuthenticationFailed(msg)

        except (jwt.InvalidTokenError,jwt.DecodeError,jwt.ExpiredSignature):            
            msg = {"status" :status.HTTP_401_UNAUTHORIZED, "message": "Token is invalid", "results":{}}
            raise exceptions.AuthenticationFailed(msg)

        return (user, token)

    def authenticate_header(self, request):
        return 'Token'