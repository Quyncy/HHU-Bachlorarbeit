"""
Ansicht für die Kurs API
"""
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from core.models import Kurs, Blatt

from .serializers import KursSerializer, BlattSerializer

@api_view(['GET'])
def kursApiOverView(request):
    api_urls = {
        'Kurs View': 'kurs-view/',
        'Kurs Detail': 'kurs-detail/<pk>',

        'Blatt View': 'blatt-view/',
        'Blatt Detail': 'blatt-detail/<pk>',
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

    def get_object(self, request, pk):
        try:
            blatt = Blatt.objects.get(pk=pk)
        except Blatt.DoesNotExist:
            return Response({'error': 'Nicht gefunden.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BlattSerializer(blatt, context={'request': request})
        return Response(serializer.data)

    def get(self, request, pk):
        blatt = Blatt.objects.get(pk=pk)
        serializer = BlattSerializer(blatt, many=False)
        return Response(serializer.data)
    
    def put(self, request, pk):
        blatt = Blatt.objects.get(pk=pk)
        serializer = BlattSerializer(blatt, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        blatt = Blatt.objects.get(pk=pk)
        blatt.delete()
        return Response("Benutzer wurde erfolgreich gelöscht.")


