"""
Serializers für die User API
"""
from core.models import (
    User, Dozent, Kursleiter, Tutor,
)

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .helpers import *



class UserSerializer(serializers.ModelSerializer):
    """ Serializer für den Benutzer """
    # password2 = serializers.CharField(style={'input_type': 'password'},write_only=True)
    password = serializers.CharField(max_length=255, style={'input_type': 'password'})

    class Meta:
        model =  User
        fields = '__all__'
        # extra_kwargs = {'password': {'write_only':True}}

        # fields = ['email', 'vorname', 'nachname', 'rolle','password', 'password2']
# So sollte die json aussehen
#     {
#     "id": 5,
#     "password": "admin132",
#     "last_login": null,
#     "is_superuser": false,
#     "rolle": "Dozent",
#     "email": "dozent@hhu.de",
#     "vorname": "Dozent",
#     "nachname": "Zwei",
#     "is_active": true,
#     "is_staff": false,
#     "groups": [],
#     "user_permissions": []
# }
    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)

    def save(self):
            email = self.validated_data['email']
            password = self.validated_data['password']
            print(password)
            rolle = self.validated_data['rolle']
            vorname = self.validated_data['vorname']
            nachname = self.validated_data['nachname']
            is_active = self.validated_data['is_active']
            is_staff = self.validated_data['is_staff']
            is_superuser = self.validated_data['is_superuser']

            # if password != password2:
            #     return Response("Falsches Passwort")

            # else:
            user = get_user_model().objects.create(
                    email=email,
                    rolle=rolle,
                    vorname=vorname,
                    nachname=nachname,
                    is_superuser=is_superuser,
                    is_active = is_active,
                    is_staff=is_staff,
                    password=password,
                )
            user.save()
            return user

    def update(self, instance, validated_data):
            """Update und return user."""
            password = validated_data.pop('password', None)
            user = super().update(instance, validated_data)

            if password:
                user.set_password(password)
                user.save()

            return user


class KursleiterSerializer(serializers.ModelSerializer):
    # tutor = TutorSerializer(many=True, read_only=True)

    class Meta:
        model = Kursleiter
        fields = '__all__' 
        # ('email', 'vorname', 'nachname','rolle',)

    def save(self):
        email = self.validated_data['email']
        password = self.validated_data['password']

        rolle = self.validated_data['rolle']

        is_superuser = self.validated_data['is_superuser']
        vorname = self.validated_data['vorname']
        nachname = self.validated_data['nachname']
        is_active = self.validated_data['is_active']
        is_staff = self.validated_data['is_staff']

        # if password != password2:
        #     return Response("Falsches Passwort")

        # else:
        kursleiter = Kursleiter.objects.create_user(
                email=email,
                rolle=rolle,
                vorname=vorname,
                nachname=nachname,
                is_superuser=is_superuser,
                is_active=is_active,
                is_staff=is_staff,
            )
        kursleiter.set_password(password)
        kursleiter.save()

        return kursleiter


################


class TutorSerializer(serializers.ModelSerializer):
    # tutor = TutorSerializer(many=True, read_only=True)

    class Meta:
        model = Tutor
        # fields = '__all__' 
        exclude = ['last_login']
        # ('email', 'vorname', 'nachname','rolle',)

    def save(self):
        email = self.validated_data['email']
        password = self.validated_data['password']

        rolle = self.validated_data['rolle']

        is_superuser = self.validated_data['is_superuser']
        vorname = self.validated_data['vorname']
        nachname = self.validated_data['nachname']
        is_active = self.validated_data['is_active']
        is_staff = self.validated_data['is_staff']

        tutor = Tutor.objects.create_user(
                email=email,
                rolle=rolle,
                vorname=vorname,
                nachname=nachname,
                is_superuser=is_superuser,
                is_active=is_active,
                is_staff=is_staff,
            )
        tutor.set_password(password)
        tutor.save()

        return tutor


################

class DozentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dozent
        fields = '__all__'


    def save(self):
        email = self.validated_data['email']
        password = self.validated_data['password']

        rolle = self.validated_data['rolle']
        is_superuser = self.validated_data['is_superuser']
        vorname = self.validated_data['vorname']
        nachname = self.validated_data['nachname']
        is_active = self.validated_data['is_active']
        is_staff = self.validated_data['is_staff']
        # groups = self.validated_data['groups'],
        # user_permissions = self.validated_data['user_permissions'],

        dozent = Dozent.objects.create_user(
                email=email,
                rolle=rolle,
                vorname=vorname,
                nachname=nachname,
                is_superuser=is_superuser,
                is_active = is_active,
                is_staff=is_staff,
            )
        dozent.set_password(password)
        dozent.save()

        return dozent

###################

# @receiver(post_save, sender=Tutor)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created and instance.rolle == "Tutor":
#         TutorProfile.objects.create(user=instance)


# @receiver(post_save, sender=Kursleiter)
# def create_kursleiter_profile(sender, instance, created, **kwargs):
#     if created and instance.rolle == "Kursleiter":
#         KursleiterProfile.objects.create(user=instance)


# @receiver(post_save, sender=Dozent)
# def create_tutor_profile(sender, instance, created, **kwargs):
#     if created and instance.rolle == "Dozent":
#         DozentProfile.objects.create(user=instance)


# @receiver(post_save, sender=get_user_model())
# def create_profile(sender, instance, created, **kwargs):
#     if created and instance.rolle == "Admin":
#         get_user_model().objects.create(instance=instance)
#     if created and instance.rolle == "Kursleiter":
#         KursleiterProfile.objects.create(user=instance)
#     if created and instance.rolle == "Tutor":
#         TutorProfile.objects.create(user=instance)
#     if created and instance.rolle == "Dozent":
#         DozentProfile.objects.create(user=instance)