from django.shortcuts import render

from .models import Genre
from .models import Artist
from .models import Song

from .serializers import GenreSerializer
from .serializers import ArtistSerializer
from .serializers import SongSerializer

from rest_framework import generics
from rest_framework import status
from rest_framework.views import Response
from rest_framework.views import APIView

class CreateGenre(generics.ListCreateAPIView):
    """
    [POST] - Create a Genre,
    [GET] - Get all Genre
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def perform_create(self, serializer):
        """save the post data when creating a foodcategory"""
        serializer.save()

class GenreDetails(generics.RetrieveUpdateDestroyAPIView):

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class CreateArtist(generics.ListCreateAPIView):
    """
    [POST] - Create an Artist,
    [GET] - Get all Artists
    """
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

    def perform_create(self, serializer):
        """save the post data when creating a foodcategory"""
        serializer.save()

class ArtistDetails(generics.RetrieveUpdateDestroyAPIView):
    '''
    [GET, PUT, DELETE] - an artist
    '''
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

class CreateSong(generics.ListCreateAPIView):
    """
    [POST] - Create Song,
    [GET] - Get all Song
    """
    queryset = Song.objects.all()
    serializer_class = SongSerializer

    def perform_create(self, serializer):
        """save the post data when creating a foodcategory"""
        serializer.save()

class SongDetails(generics.RetrieveUpdateDestroyAPIView):
    '''
    [GET, PUT, DELETE] - a song
    '''
    queryset = Song.objects.all()
    serializer_class = SongSerializer
