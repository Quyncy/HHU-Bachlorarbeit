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
from kurs.serializers import KursSerializer



class UserSerializer(serializers.ModelSerializer):
    """ Serializer für den Benutzer """

    class Meta:
        model =  User
        fields = '__all__'
        # extra_kwargs = {'password': {'write_only':True}}
        # fields = ['email', 'vorname', 'nachname', 'rolle','password', 'password2']


    ##########?????????
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
        print(user.rolle)
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
    # kurs = KursSerializer(many=True, read_only=True)
    class Meta:
        model = Kursleiter
        fields = '__all__' 
        # ('email', 'vorname', 'nachname','rolle',)

    def create(self, validated_data):
        kurs=self.validated_data['kurs']
        print(kurs)
        if kurs!=None:
            kurs = Kurs.objects.get(kurs=self.validated_data['kurs'])

        password=self.validated_data['password']

        kursleiter = Kursleiter(
            email = self.validated_data['email'],
            vorname = self.validated_data['vorname'],
            nachname = self.validated_data['nachname'],
            rolle = self.validated_data['rolle'],
            is_active = self.validated_data['is_active'],
            is_kursleiter = self.validated_data['is_kursleiter'],
            password = self.validated_data['password'],
            kurs = kurs,
            # is_superuser = self.validated_data['is_superuser'],
            # groups, 
            # user_permissions,
        )
        kursleiter.set_password(password)
        kursleiter.save()

        return kursleiter






class TutorSerializer(serializers.ModelSerializer):
    # tutor = TutorSerializer(many=True, read_only=True)
    # user = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # kurs = KursSerializer(many=True, read_only=True)

    class Meta:
        model = Tutor
        fields = '__all__' 
        # exclude = ['last_login']


    def create(self, validated_data):
        # user_permissions = User.objects.create(**validated_data)
        # kurs = Kurs.objects.get(kurs=self.validated_data['kurs'])
        password=self.validated_data['password']

        print('ich bin hier')
        # tutor = Tutor() # or Tutor.objects.create()
        tutor = Tutor.objects.create_user(
                email = self.validated_data['email'],
                vorname = self.validated_data['vorname'],
                nachname = self.validated_data['nachname'],
                rolle = self.validated_data['rolle'],
                is_active = self.validated_data['is_active'],
                is_tutor = self.validated_data['is_tutor'],
                is_superuser = self.validated_data['is_superuser'],
                tutor_id=self.validated_data['tutor_id'],
                arbeitsstunden=self.validated_data['arbeitsstunden'],

                # is_admin = self.validated_data['is_admin'],
                # kurs=self.validated_data['kurs'],
                # kurs=kurs,
                # groups
                # user_permissions
            )
        tutor.set_password(password)
        tutor.save()

        return tutor





class DozentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dozent
        fields = '__all__'


    def create(self, validated_data):  
        # groups = self.validated_data['groups'],
        # user_permissions = self.validated_data['user_permissions'],
        password=self.validated_data['password']

        dozent = Dozent.objects.create(
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
        dozent.set_password(password)
        dozent.save()

        # DozentProfile.objects.create(user=dozent)

        return dozent





##########################



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


class KursleiterProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = KursleiterProfile
        fields = '__all__'

    # def create(self, validated_data):
    #     kursleiterprofile = KursleiterProfile(
            
    #     )