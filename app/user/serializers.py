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

    class Meta:
        model =  User
        fields = '__all__'
        # extra_kwargs = {'password': {'write_only':True}}
        # fields = ['email', 'vorname', 'nachname', 'rolle','password', 'password2']

    def create(self, validated_data):
        
        user = User.objects.create_user(
                email = self.validated_data['email'],
                vorname = self.validated_data['vorname'],
                nachname = self.validated_data['nachname'],
                rolle = self.validated_data['rolle'],
                is_active = self.validated_data['is_active'],
                is_staff = self.validated_data['is_staff'],
                is_superuser = self.validated_data['is_superuser'],
                is_admin = self.validated_data['is_admin'],
                is_tutor = self.validated_data['is_tutor'],
                is_kursleiter = self.validated_data['is_kursleiter'],
                is_dozent = self.validated_data['is_dozent'],
        )
        user.set_password(self.validated_data['password'])
        user.save()

        # return get_user_model().objects.create_user(**validated_data)
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

    def create(self, validated_data):
        kurs=self.validated_data['kurs']
        print('TEST: serializers.py')
        print(kurs)
        user = Kursleiter.objects.create_user(
            email = self.validated_data['email'],
            vorname = self.validated_data['vorname'],
            nachname = self.validated_data['nachname'],
            rolle = self.validated_data['rolle'],
            is_active = self.validated_data['is_active'],
            is_staff = self.validated_data['is_staff'],
            is_superuser = self.validated_data['is_superuser'],
            # groups, 
            # user_permissions,
        )
        user.set_password(self.validated_data['password'])
        user.save()

        print(user)

        # KursleiterProfile.objects.create(user=kursleiter)

        return user


class KursleiterProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = KursleiterProfile
        fields = '__all__'

    # def create(self, validated_data):
    #     kursleiterprofile = KursleiterProfile(
            
    #     )



################


class TutorSerializer(serializers.ModelSerializer):
    # tutor = TutorSerializer(many=True, read_only=True)
    # user = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Tutor
        fields = '__all__' 
        # exclude = ['last_login']

    # def create(self, validated_data):
    #     """Create and return a user with encrypted password."""
    #     print(validated_data)
    #     # tutor = Tutor.objects.create_user(**validated_data)
    #     # print(tutor.email)
    #     return Tutor.objects.create_user(**validated_data)

    def create(self, validated_data):
        tutor = Tutor(
                email = self.validated_data['email'],
                vorname = self.validated_data['vorname'],
                nachname = self.validated_data['nachname'],
                rolle = self.validated_data['rolle'],
                is_active = self.validated_data['is_active'],
                is_staff = self.validated_data['is_staff'],
                is_superuser = self.validated_data['is_superuser'],
                is_admin = self.validated_data['is_admin'],
                is_tutor = self.validated_data['is_tutor'],
                is_kursleiter = self.validated_data['is_kursleiter'],
                is_dozent = self.validated_data['is_dozent'],
            )
        tutor.set_password(self.validated_data['password'])
        tutor.save()

        # TutorProfile.objects.create(
        #     user=tutor, 
        #     tutor_id=self.validated_data['tutor_id'],
        #     kurs=self.validated_data['kurs'],
        # )

        return tutor


class TutorProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = TutorProfile
        fields = '__all__'

        # def create(self, validated_data):
        #     tutorprofile = TutorProfile(
        #         user=self.validated_data['user'],
        #         kurs=self.validated_data['kurs'],
        #         tutor_id=self.validated_data['tutor_id'],
        #         arbeitsstunden=self.validated_data['arbeitsstunden'],
        #     )
        #     tutorprofile.save()

        #     return tutorprofile



################

class DozentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dozent
        fields = '__all__'


    def create(self, validated_data):  
        # groups = self.validated_data['groups'],
        # user_permissions = self.validated_data['user_permissions'],

        dozent = Dozent(
                email = self.validated_data['email'],
                rolle = self.validated_data['rolle'],
                vorname = self.validated_data['vorname'],
                nachname = self.validated_data['nachname'],
                is_active = self.validated_data['is_active'],
                is_staff = self.validated_data['is_staff'],
                is_superuser = self.validated_data['is_superuser'],
                is_admin = self.validated_data['is_admin'],
                is_tutor = self.validated_data['is_tutor'],
                is_kursleiter = self.validated_data['is_kursleiter'],
                is_dozent = self.validated_data['is_dozent'],
            )
        dozent.set_password(self.validated_data['password'])
        dozent.save()

        DozentProfile.objects.create(user=dozent)

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