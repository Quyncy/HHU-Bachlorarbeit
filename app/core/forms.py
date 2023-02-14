from django import forms
from django.utils.translation import gettext_lazy as _

from .models import *
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm



# class AuthenticationForm(AuthenticationForm):
#     class Meta:
#         model = User
#         fields = '__all__'


# class CostumUserCreationForm(UserCreationForm):
#     # class Meta:
#     #     model = User
#     #     fields= '__all__'
#     #     # exclude = ['password', 'last_login',]

#     """A form for creating new users. Includes all the required
#     fields, plus a repeated password."""
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         # exclude = ('password', 'last_login',)
#         fields = '__all__'
#         # fields = ('email', )

#     def clean_password2(self):
#         # Check that the two password entries match
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError("Passwords don't match")
#         return password2

#     def save(self, commit=True):
#         # Save the provided password in hashed format
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user


# class CustomUserChangeForm(UserChangeForm):
#     password = ReadOnlyPasswordHashField()

#     class Meta:
#         model = User
#         fields = ('email', 'password', 'is_active', 'is_admin')

#     def clean_password(self):
#         # Regardless of what the user provides, return the initial value.
#         # This is done here, rather than on the field, because the
#         # field does not have access to the initial value
#         return self.initial["password"]


class AuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = '__all__'


class CostumUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields= '__all__'
        # exclude = ['password', 'last_login',]


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email",)


# class SignupForm(forms.ModelForm):
#     """user signup form"""
#     password = forms.CharField(widget=forms.PasswordInput())

#     class Meta:
#         model = get_user_model()
#         fields = ('email', 'password',)

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=200, required=True)
    password = forms.CharField(widget=forms.PasswordInput)



class KursleiterForm(UserCreationForm):
    class Meta:
        model = Kursleiter
        fields ='__all__'
        # exclude=['rolle', 'last_login', 'groups', 'user_permissions',
        # 'is_staff', 'is_admin','is_superuser', 'is_dozent', 'is_tutor',]
        

class TutorForm(UserCreationForm):
    class Meta:
        model = Tutor
        fields = '__all__'
        # exclude=['last_login', 'groups', 'user_permissions',
        # 'is_staff', 'is_admin','is_superuser', 'is_dozent', 'is_kursleiter',]



class DozentForm(forms.ModelForm):
    class Meta:
        model = Dozent
        fields = '__all__'
        #exclude=['rolle', 'last_login', 'groups', 'user_permissions', 'password']
        


class KursForm(forms.ModelForm):
    class Meta:
        model = Kurs
        fields = '__all__'
       


class BlattForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BlattForm, self).__init__(*args, **kwargs)
        # help_text kann aktualisiert werden
        self.fields['ass_name'].help_text = "Übungsblatt Nr. (update)"

    class Meta:
        model = Blatt
        exclude = ('',) # == fields = '__all__'



class BlattKorrekturForm(forms.ModelForm):
    
    class Meta:
        model = BlattKorrektur
        fields = '__all__'