from django.contrib import admin
from django.urls import path, include
from . views import*

# from cassandra.cluster import Cluster
# cluster = Cluster(['127.0.0.1'], control_connection_timeout=10,  port=9042)
# session = cluster.connect('tutorialspoint')
# try:
    # query = session.execute("""ALTER TABLE example_model DROP emp_email""")
    # print('query', query)
    # query = session.execute("ALTER TABLE user_model DROP profile")
    # print('query', query)
    # query = session.execute("ALTER TABLE group_model DROP admin_id")
    # print('query', query)
    # query = session.execute("ALTER TABLE message_model DROP read_by")
    # print('query', query)
    # print('query')
# except:
#     pass

urlpatterns = [
    path('', homepage, name='home'),

    # onbord
    path('onbord', OnbordView.as_view()),

    # api User
    path('user_register', UserRegisterView.as_view()),
    path('user_login', UserLoginView.as_view()),
    path('otp_verify', OTPVerifyView.as_view()),
    path('user_logout', LogoutView.as_view()),
   
]
