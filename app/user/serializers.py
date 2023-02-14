"""
Serializers für die User API
"""
from core.models import (
    User, Dozent, Kursleiter, Tutor,
)

from django.contrib.auth import get_user_model as User

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .helpers import *
from kurs.serializers import KursSerializer

from guardian.shortcuts import assign_perm




class UserSerializer(serializers.ModelSerializer):
    """ Serializer für den Benutzer """

    class Meta:
        model =  User
        fields = '__all__'
        # extra_kwargs = {'password': {'write_only':True}}
        # fields = ['email', 'vorname', 'nachname', 'rolle','password', 'password2']


    ##########?????????
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        # (
        #         email = self.validated_data['email'],
        #         vorname = self.validated_data['vorname'],
        #         nachname = self.validated_data['nachname'],
        #         rolle = self.validated_data['rolle'],
        #         is_active = self.validated_data['is_active'],
        #         is_staff = self.validated_data['is_staff'],
        #         is_superuser = self.validated_data['is_superuser'],
        #         is_admin = self.validated_data['is_admin'],
        #         is_tutor = self.validated_data['is_tutor'],
        #         is_kursleiter = self.validated_data['is_kursleiter'],
        #         is_dozent = self.validated_data['is_dozent'],
        # )
        # print(user.rolle)
        # user.set_password(self.validated_data['password'])
        # user.save()

        # return get_user_model().objects.create_user(**validated_data)
        Token.objects.create(user)

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
        groups = validated_data.pop('groups', None)
        user_permissions = validated_data.pop('user_permissions', None)
        kurs = validated_data.pop('kurs', None)
    
        kursleiter = Kursleiter.objects.create(**validated_data)

        kursleiter.kurs = kurs
        assign_perm('view_kurs', kursleiter, kurs) # kursleiter eigenen Kurs sehen
        assign_perm('change_kurs', kursleiter, kurs)
        assign_perm('delete_kurs', kursleiter, kurs)

        assign_perm('view_kursleiter', kursleiter, kursleiter)  # kursleiter kann eigenes Profil sehen und bearbeiten
        assign_perm('change_kursleiter', kursleiter, kursleiter)

        
        # assign_perm('view_tutor', kursleiter, tutor) # kursleiter kann Tutoren zum eigenen Kurs hinzufügen, bearbeiten und löschen
        # assign_perm('change_tutor', kursleiter, tutor)
        # assign_perm('delete_tutor', kursleiter, tutor)
        # assign_perm('view_kursletutor', kursleiter, kursletutor)

        kursleiter.save()

        Token.objects.create(kursleiter)

        return kursleiter






class TutorSerializer(serializers.ModelSerializer):
    # tutor = TutorSerializer(many=True, read_only=True)
    # user = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # tutor = KursSerializer(many=True, read_only=True)

    class Meta:
        model = Tutor
        fields = '__all__'
        # fields = ('email', 'vorname', 'nachname', 'tutor_id', 'kurs', 'arbeitsstunden',)
        # exclude = ['last_login']


    def create(self, validated_data):
        groups = validated_data.pop('groups', None)
        user_permissions = validated_data.pop('user_permissions', None)
        kurs = validated_data.pop('kurs', None)

        # tutor = Tutor() # or Tutor.objects.create()
        tutor = Tutor.objects.create_user(**validated_data)   
        #tutor = Tutor.objects.create(
        #         email = validated_data['email'],
        #         vorname = validated_data['vorname'],
        #         nachname = validated_data['nachname'],
        #         rolle = validated_data['rolle'],
        #         is_active = validated_data['is_active'],
        #         is_staff = validated_data['is_staff'],
        #         is_superuser = validated_data['is_superuser'],
        #         is_admin = validated_data['is_admin'],
        #         is_tutor = validated_data['is_tutor'],
        #         is_kursleiter = validated_data['is_kursleiter'],
        #         is_dozent = validated_data['is_dozent'],
        #         tutor_id = validated_data['tutor_id'],
        #         arbeitsstunden = validated_data['arbeitsstunden'],
        #         # kurs = kurs,
        #         # groups = groups,
        #         # user_permissions = user_permissions,
        # )
        tutor.kurs = kurs
        
        # gebe dem erstellten Tutor die Erlaubnis diesen Kurs zu sehen
        assign_perm('view_kurs', tutor, kurs)
        tutor.save()
        assign_perm('view_user', tutor, tutor)
        tutor.save()
        Token.objects.create(tutor)

        return tutor





class DozentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dozent
        fields = '__all__'


    def create(self, validated_data):  
        groups = validated_data.pop('groups', None)
        user_permissions = validated_data.pop('user_permissions', None)

        dozent = Dozent.objects.create(**validated_data)

        Token.objects.create(dozent)

        return dozent



###########


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type':'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = ('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs




##########################



# class TutorProfileSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = TutorProfile
#         fields = '__all__'

#         # def create(self, validated_data):
#         #     tutorprofile = TutorProfile(
#         #         user=self.validated_data['user'],
#         #         kurs=self.validated_data['kurs'],
#         #         tutor_id=self.validated_data['tutor_id'],
#         #         arbeitsstunden=self.validated_data['arbeitsstunden'],
#         #     )
#         #     tutorprofile.save()

#         #     return tutorprofile


# class KursleiterProfileSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = KursleiterProfile
#         fields = '__all__'

#     # def create(self, validated_data):
#     #     kursleiterprofile = KursleiterProfile(
            
#     #     )