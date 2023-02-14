"""
Ansicht für die Kurs API
"""
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from core.models import Kurs, Blatt, BlattKorrektur

from .serializers import KursSerializer, BlattSerializer, BlattKorrekturSerializer

@api_view(['GET'])
def kursApiOverView(request):
    api_urls = {
        'Kurs erstellen': 'create-kurs/',
        'Kurs Liste': 'list-kurs/',
        'Kurs Detail': 'get-kurs/<pk>',

        'Blatt erstellen': 'create-blatt/',
        'Blatt Liste': 'list-blatt/',
        'Blatt Detail': 'get-blatt/<pk>',
    }

    return Response(api_urls)


##############################


class CreateKursView(generics.CreateAPIView):
    serializer_class = KursSerializer
    permission_class = []


class KursList(generics.ListCreateAPIView):
    """
    Liste aller Kurse und erstellt neuen Kurs
    """
    queryset = Kurs.objects.all()
    serializer_class = KursSerializer



class KursDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Enthält, updatet und löscht Kurs
    """
    queryset = Kurs.objects.all()
    serializer_class = KursSerializer
    permission_classes = []

    def get(self, request, pk):
        kurs = Kurs.objects.get(pk=pk)
        serializer = KursSerializer(kurs, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        kurs = Kurs.objects.get(pk=pk)
        serializer = KursSerializer(kurs, request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        kurs = Kurs.objects.get(pk=pk)
        kurs.delete()
        return Response("Kurs wurde erfolgreich gelöscht.", status=status.HTTP_204_NO_CONTENT)

# class KursDetail(generics.RetrieveUpdateDestroyAPIView):
#     """
#     Enthält, updatet und löscht Kurs
#     """
#     queryset = Kurs.objects.all()
#     serializer_class = KursSerializer
#     permission_classes = []

    

###############################


class CreateBlattView(generics.CreateAPIView):
    serializer_class = BlattSerializer
    permission_class = []


class BlattList(generics.ListCreateAPIView):
    """
    Liste aller Blätter und erstellt neues Blatt
    """
    queryset = Blatt.objects.all()
    serializer_class = BlattSerializer


class BlattDetail(APIView):
    """
    Erhält, updatet und löscht Benutzer
    """
    permission_classes = []

    # def get_object(self, request, pk):
    #     try:
    #         blatt = Blatt.objects.get(pk=pk)
    #     except Blatt.DoesNotExist:
    #         return Response({'error': 'Nicht gefunden.'}, status=status.HTTP_404_NOT_FOUND)

    #     serializer = BlattSerializer(blatt, context={'request': request})
    #     return Response(serializer.data)

    def get(self, request, pk):
        blatt = Blatt.objects.get(pk=pk)
        serializer = BlattSerializer(blatt, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        blatt = Blatt.objects.get(pk=pk)
        serializer = BlattSerializer(blatt, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        blatt = Blatt.objects.get(pk=pk)
        blatt.delete()
        return Response("Übungsblatt wurde erfolgreich gelöscht.", )


class CreateBlattKorrekturView(generics.CreateAPIView):
    serializer_class = BlattKorrekturSerializer
    permission_classes = []


class ListBlattKorrekturView(generics.ListAPIView):
    queryset = BlattKorrektur.objects.all()
    serializer_class = BlattKorrekturSerializer
    permission_classes = []


class BlattKorrekturDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BlattKorrekturSerializer
    permission_classes = []
