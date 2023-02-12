# from .models import User
from django.contrib.auth.backends import ModelBackend
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password



class EmailBackend(ModelBackend): 

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


        # if username is None:
        #     username = kwargs.get(User.USERNAME_FIELD)
        #     print(username)
        # try:
        #     case_insensitiv_username_field = '{}__iexact'.format(User.USERNAME_FIELD)
        #     print(case_insensitiv_username_field)
        #     user = User._default_manager.get(**{case_insensitiv_username_field: username})
        # except User.DoesNotExist:
        #     User.set_password(password)

        # else:
        #     if user.check_password(password) and self.user_can_authenticate:
        #         print('check password')
        #         return user


        

    def get_user(self, id):
        User = get_user_model()
        try:
            print('Emailbackend: get_user: ')
            print(User.objects.get(id=id))
            return User.objects.get(id=id) # <-- tried to get by email here
        except User.DoesNotExist:
            return None