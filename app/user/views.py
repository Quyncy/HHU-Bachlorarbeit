from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from .serializers import (
    UserSerializer, KursleiterSerializer,
    DozentSerializer, TutorSerializer, AuthTokenSerializer
)
# DozentProfilSerializer

from rest_framework.authtoken.models import Token

from user.permissions import AdminOrReadOnly

from core.models import (
    Kursleiter, Dozent, Tutor
    # DozentProfile, ,
)


@api_view(['GET',])
def apiOverView(request):
    api_urls = {
        'User erstellen': 'create-user/',
        'User Liste': 'list-user/',
        # 'User erhalten, updaten und löschen': 'detail-user/<pk>',
        'User erhalten': 'get-user/<pk>/',
        'User bearbeiten': 'update-user/<pk>/',
        'User löschen': 'delete-user/<pk>/',

        'Kursleiter erstellen': 'create-kursleiter/',
        'Kursleiter Liste': 'list-kursleiter/',
        # 'Kursleiter erhalten, updaten und löschen': 'detail-kursleiter/<pk>',
        'Kursleiter erhalten': 'get-kursleiter/<pk>/',
        'Kursleiter bearbeiten': 'update-kursleiter/<pk>/',
        'Kursleiter löschen': 'delete-kursleiter/<pk>/',

        'Dozent erstellen': 'create-dozent/',
        'Dozent Liste': 'list-dozent/',
        # 'Dozent erhalten, updaten und löschen': 'detail-dozent/<pk>',
        'Dozent erhalten': 'get-dozent/<pk>/',
        'Dozent bearbeiten': 'update-dozent/<pk>/',
        'Dozent löschen': 'delete-dozent/<pk>/',
    }
    return Response(api_urls)


# @api_view(['POST'])
# def logout_view(request):
#     if request.method == 'POST':
#         request.user.auth_token.delete()
#         return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
# @permission_classes([AdminPerm]) # eigtl hätte ich hier die Recht haben müssen
def register_view(request):
    data = {}
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            data['response'] = "Registierung erfolgreich"
            data['email'] = user.email
            data['vorname'] = user.vorname
            data['nachname'] = user.nachname

            token = Token.objects.get(user=user).key

            data['token'] = token
            print(token)

        else:
            data = serializer.errors

        return Response(data, status=status.HTTP_201_CREATED)





@api_view(['POST',])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response("Token wurde nicht gelöscht.")

#####################################

class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes=[]


class UserListView(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes=[]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes=[]


# class UserDetailView(APIView):
#     permission_classes=[AdminOrReadOnly]

#     def get(self, request, pk):
#         user = get_user_model().objects.get(pk=pk)
#         serializer = UserSerializer(user, many=False)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         user = get_user_model().objects.get(pk=pk)
#         serializer = UserSerializer(user, request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST )

#     def delete(self, request, pk):
#         user = get_user_model().objects.get(pk=pk)
#         user.delete()
#         return Response("User wurde erfolgreich gelöscht.")





class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES



class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = []

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user







###################################


class CreateKursleiterView(generics.CreateAPIView):
    # KursleiterProfile
    serializer_class = KursleiterSerializer
    permission_classes = []


class KursleiterListView(generics.ListAPIView):
    # KursleiterProfile
    queryset = Kursleiter.objects.all()
    serializer_class = KursleiterSerializer

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = KursleiterSerializer(queryset, many=True)
        return Response(serializer.data)


class KursleiterDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Kursleiter.objects.all()
    serializer_class = KursleiterSerializer
    permission_classes = []


# class KursleiterDetailView(APIView):

#     def get(self, request, pk):
#         user = Kursleiter.objects.get(pk=pk)
#         serializer = KursleiterSerializer(user, many=False)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         user = Kursleiter.objects.get(pk=pk)
#         serializer = KursleiterSerializer(user, request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         user = Kursleiter.objects.get(pk=pk)
#         user.delete()
#         return Response("Kursleiter wurde erfolgreich gelöscht.", status=status.HTTP_204_NO_CONTENT)


# ########


# class CreateKursleiterProfileView(generics.CreateAPIView):
#     serializer_class = KursleiterProfileSerializer
#     permission_classes=[]


# class KursleiterProfileListView(generics.ListAPIView):
#     queryset = KursleiterProfile.objects.all()
#     serializer_class = KursleiterSerializer




#################################################




class CreateTutorView(generics.CreateAPIView):
    serializer_class = TutorSerializer
    permission_classes = []


class TutorListView(generics.ListAPIView):
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer
    permission_classes = []


class TutorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer
    permission_classes = []


# class TutorDetailView(APIView):
#     permission_classes = [AdminOrReadOnly]

#     def get(self, request, pk):
#         user = Tutor.objects.get(pk=pk)
#         serializer = TutorSerializer(user, many=False)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def put(self, request, pk):
#         tutor = Tutor.objects.get(pk=pk)
#         serializer = TutorSerializer(tutor, request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST )

#     def delete(self, request, pk):
#         user = Tutor.objects.get(pk=pk)
#         user.delete()
#         return Response("Tutor wurde erfolgreich gelöscht.", status=status.HTTP_204_NO_CONTENT)



##############



# class TutorProfileView(generics.CreateAPIView):
#     serializer_class = TutorProfileSerializer
#     permission_classes=[]


# class TutorProfileListView(generics.ListAPIView):
#     queryset = TutorProfile.objects.all()
#     serializer_class = TutorProfileSerializer
#     permission_classes = []








    
#################################################




class CreateDozentView(generics.CreateAPIView):
    serializer_class = DozentSerializer
    permission_classes = []


class DozentListView(generics.ListAPIView):
    queryset = Dozent.objects.all()
    serializer_class = DozentSerializer


class DozentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dozent.objects.all()
    serializer_class = DozentSerializer
    permission_classes =[]


# class DozentDetailView(APIView):

#     def get(self, request, pk):
#         user = Dozent.objects.get(pk=pk)
#         serializer = DozentSerializer(user, many=False)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def put(self, request, pk):
#         user = Dozent.objects.get(pk=pk)
#         serializer = DozentSerializer(user, request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST )

#     def delete(self, request, pk):
#         user = Dozent.objects.get(pk=pk)
#         user.delete()
#         return Response("Dozent wurde erfolgreich gelöscht.", status=status.HTTP_204_NO_CONTENT)

