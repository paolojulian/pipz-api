from django.db import models

# Create your models here.

class Genre(models.Model):
    ''' The genre of the song '''
    name = models.CharField(max_length=100, blank=False, unique=True)

    def __str__(self):
        return "{}".format(self.name)

    def response_created(self):
        return f"{self.name} has been created"

class Artist(models.Model):
    ''' The artist of the song '''
    name = models.CharField(max_length=100, blank=False, unique=True)

    def __str__(self):
        return "{}".format(self.name)

    def response_created(self):
        return f"{self.name} has been created"

class Song(models.Model):
    ''' Song '''
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

    name = models.CharField(max_length=100, blank=False)
    audio_path = models.TextField()

    class Meta:
        unique_together = ['name', 'artist', 'genre']

    def __str__(self):
        return f"name: {self.name}, audio_path: {self.audio_path}, genre: {self.genre}, artist: {self.artist}"

    def response_created(self):
        return f"{self} has been successfully created"


