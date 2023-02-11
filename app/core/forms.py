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
    # class Meta:
    #     model = User
    #     fields= '__all__'
    #     # exclude = ['password', 'last_login',]

    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        exclude = ('password', 'last_login',)
        # fields = '__all__'
        # fields = ('email', )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("email",)



class LoginForm(forms.Form):
    email = forms.EmailField(max_length=200, required=True)
    password = forms.CharField(widget=forms.PasswordInput)


###############################


class KursleiterForm(forms.ModelForm):
    class Meta:
        model = Kursleiter
        # fields ='__all__'
        exclude=['rolle', 'last_login', 'groups', 'user_permissions',
        'is_staff', 'is_admin','is_superuser', 'is_dozent', 'is_tutor',]
        

########################


class TutorForm(forms.ModelForm):
    class Meta:
        model = Tutor
        # fields = '__all__'
        exclude=['last_login', 'groups', 'user_permissions',
        'is_staff', 'is_admin','is_superuser', 'is_dozent', 'is_kursleiter',]


class TutorProfileForm(forms.ModelForm):
    class Meta:
        model = TutorProfile
        fields = '__all__'
        # fields = ['user, tutor_id, kurs, arbeitsstunden']

        
##############################


class DozentForm(forms.ModelForm):
    class Meta:
        model = Dozent
        fields = '__all__'
        #exclude=['rolle', 'last_login', 'groups', 'user_permissions', 'password']
        
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