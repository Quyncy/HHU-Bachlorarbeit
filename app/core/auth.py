# from .models import User
from django.contrib.auth.backends import ModelBackend
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password



class EmailBackend(ModelBackend): 
    """
    Backend zum authentifizieren der Email-Adresse und Password
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(email=username)
            print('auth.py1: '+ str(user.email))
            print('auth.py2: '+ str(make_password(password)))
            print('auth.py3: '+ str(user.check_password(password)))
            if user.check_password(password):
                print('auth.py4: ' + str(user))
                print(user.id)
                return user
            return None
        except User.DoesNotExist:
            return None 

    def get_user(self, id):
        User = get_user_model()
        try:
            print('Emailbackend: get_user: ')
            print(User.objects.get(id=id))
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return None