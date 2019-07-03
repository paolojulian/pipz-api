# music/serializers.py

from rest_framework import serializers
from .models import Genre
from .models import Artist
from .models import Song

class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('id', 'name')

class ArtistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Artist
        fields = ('id', 'name')

class SongSerializer(serializers.ModelSerializer):

    artist_name = serializers.CharField(source='artist.name', read_only=True)
    genre_name = serializers.CharField(source='genre.name', read_only=True)
    class Meta:
        model = Song
        fields = ('id', 'name', 'audio_path', 'artist', 'artist_name', 'genre', 'genre_name')
