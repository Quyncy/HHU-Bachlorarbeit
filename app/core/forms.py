from django import forms
from django.utils.translation import gettext_lazy as _

from core.models import *

#########
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm


class AuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = '__all__'


class CostumUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        exclude = ['password', 'last_login',]


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("email",)


# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

#     class Meta:
#         model = User
#         fields = ('email', 'password1', 'password2', )


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=200, required=True)
    password = forms.CharField(widget=forms.PasswordInput)


################################## 


class UserForm(forms.ModelForm):
    """ Bei Admin eingaben werden die fields ignoriert """
    class Meta:
        model = User
        exclude=['rolle', 'last_login', 'groups', 'user_permissions', 'password']

        labels = {
            'email': _('Email'),
            'vorname': _('Vorname'),
            'nachname': _('Nachname'),
        }


class KursleiterForm(forms.ModelForm):
    class Meta:
        model = Kursleiter
        exclude=['rolle', 'last_login', 'groups', 'user_permissions', 'password']

        labels = {
            'email': _('Email'),
            'vorname': _('Vorname'),
            'nachname': _('Nachname'),
            'kurs_name': _('Kurs'),
            'role': _('Rolle'),
        }


# class KursleiterProfileForm(forms.Modelform):
#     class Meta:
#         model = KursleiterProfile
#         fields = '__all__'
#         # exclude = ['']


########################


class TutorForm(forms.ModelForm):
    class Meta:
        model = Tutor
        fields = '__all__'
    
        # exclude=['rolle', 'last_login', 'groups', 'user_permissions', 'password']


class TutorProfileForm(forms.ModelForm):
    class Meta:
        model = TutorProfile
        fields = '__all__'
        # fields = ['user, tutor_id, kurs, arbeitsstunden']

        
##############################


class DozentForm(forms.ModelForm):
    class Meta:
        model = Dozent
        # fields = '__all__'
        exclude=['rolle', 'last_login', 'groups', 'user_permissions', 'password']
        
        # labels = {
        #     'title': _('Titel'),
        #     'vorname': _('Vorname'),
        #     'nachname': _('Nachname'),
        # }

        # error_messages = {
        #     'titel':{
        #         'required': _('Title has to be choosen')
        #     },
        #     'vorname':{
        #         'required': _('First name has to be entered')
        #     },
        #     'nachname': _('Last name has to be entered')
        # },


############################


class KursForm(forms.ModelForm):
    class Meta:
        model = Kurs
        fields = '__all__'
        # exclude=['dozent']

        # labels := Bezeichnung
        # labels = {
        #     'kurs': _('Kursname eingeben'),
        #     'beschreibung': _('Beschreibung eingegeben'),
        #     'kursleiter': _('Kursleiter eingeben'),
        # }
        # error_messages = {
        #     fields : {
        #         'kurs': {
        #             'required': _('Module name has to be entered')
        #         },
        #         'beschreibung': {
        #             'required': _('Description has to be entered')
        #         },
        #         'Kursleiter': {
        #             'required': _('Teacher has to be entered')
        #         },
        #     }
        # }


class BlattForm(forms.ModelForm):
    class Meta:
        model = Blatt
        fields = '__all__'


# class TutorProfileForm(forms.ModelForm):
#     class Meta:
#         model=TutorProfile
#         fields='__all__'

#         label = {
#             'user': _('Vorname'),
#             'tutor_id': _('ID'),
#             'kurs': _('Kurs'),
#             'arbeitsstunden': _('Arbeitsstunden'),
#             'anzahl_korrekturen': _('Anzahl Korrekturen'),
#         }
#         error_messages = {
#             'user':{
#                 'required': ('Vorname angeben')
#             }
#         }