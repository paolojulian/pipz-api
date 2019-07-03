#music/tests.py

from django.test import TestCase

from .models import Genre
from .models import Artist
from .models import Song

from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

client = APIClient()

class CreateGenreTestCase(TestCase):
    '''
    Creation of Genre
    '''
    def setUp(self):
        self.genre = Genre(name="Pop")

    def test_model_can_create_a_genre(self):
        old_count = Genre.objects.count()
        self.genre.save()
        new_count = Genre.objects.count()

        self.assertNotEqual(old_count, new_count)


    def test_music_can_create_a_genre(self):
        data = {
            "name": "Pop"
        }
        response = client.post(
            reverse('genre'),
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_music_can_create_empty_genre(self):
        data = {
            "name": ""
        }
        response = client.post(
            reverse('genre'),
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_music_can_create_wrong_genre(self):
        data = {
            "test": "test"
        }
        response = client.post(
            reverse('genre'),
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class GenreRetrieveUpdateDeleteTestCase(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name="Pop")

    def test_music_can_get_a_valid_genre(self):
        response = client.get(
            reverse('genre_details', kwargs={'pk': self.genre.id}),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_music_can_delete_a_genre(self):
        response = client.delete(
            reverse('genre_details', kwargs={'pk': self.genre.id}),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_music_can_update_a_genre(self):
        change_genre = {
            'name': 'Rock'
        }
        response = client.put(
            reverse('genre_details', kwargs={'pk': self.genre.id}),
            change_genre,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class CreateArtistTestCase(TestCase):
    '''
    This class defines the test case for creating an artist
    '''

    def setUp(self):
        self.artist = Artist(name="Pipz")

    def test_model_can_create_an_artist(self):
        old_count = Artist.objects.count()
        self.artist.save()
        new_count = Artist.objects.count()

        self.assertNotEqual(old_count, new_count)

    def test_music_can_create_an_artist(self):
        data = {
            'name': 'Pipz'
        }
        response = client.post(
            reverse('artist'),
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class ArtistRetrieveUpdateDeleteTestCase(TestCase):
    '''
    [GET, PUT, DELETE] artist
    '''
    def setUp(self):
        self.artist = Artist.objects.create(name='Pipz')

    def test_music_can_get_a_valid_artist(self):
        response = client.get(
            reverse('artist_details', kwargs={'pk': self.artist.id}),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_music_can_delete_an_artist(self):
        response = client.delete(
            reverse('artist_details', kwargs={'pk': self.artist.id}),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_music_can_update_an_artist(self):
        change_artist = {
            'name': 'Kiel'
        }
        response = client.put(
            reverse('artist_details', kwargs={'pk': self.artist.id}),
            change_artist,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class CreateSongTestCase(TestCase):
    '''
    This class defines the test case for creating a music
    '''
    def setUp(self):
        self.genre = Genre.objects.create(name="Pop")
        self.artist = Artist.objects.create(name="Pipz")
        self.artist2 = Artist.objects.create(name="Kiel")
        self.song = Song(
            name="Music",
            audio_path="Test.mp3",
            genre_id=self.genre.id,
            artist_id=self.artist.id
        )

    def test_model_can_create_a_song(self):
        old_count = Song.objects.count()
        self.song.save()
        new_count = Song.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_music_can_create_a_song(self):
        song_data = {
            'name': 'Redbone',
            'audio_path': 'Test.mp3',
            'genre': self.genre.id,
            'artist': self.artist.id
        }

        response = client.post(
            reverse('song'),
            song_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_music_can_create_two_songs_same_name_diff_artist(self):
        ''' Song can have the same name with different artist or different genre'''
        self.song.save()
        song_data = {
            'name': 'Music',
            'audio_path': 'Test.mp3',
            'genre': self.genre.id,
            'artist': self.artist2.id
        }
        response = client.post(
            reverse('song'),
            song_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_music_cannot_create_duplicate_song(self):
        ''' Song cannot create a duplicate song (Same name, artist and genre)'''
        self.song.save()
        song_data = {
            'name': 'Music',
            'audio_path': 'Test.mp3',
            'genre': self.genre.id,
            'artist': self.artist.id
        }
        response = client.post(
            reverse('song'),
            song_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class RetrieveUpdateDeleteSongTestCase(TestCase):
    '''
    This class defines the test case for retrieving a music
    '''
    def setUp(self):
        self.genre = Genre.objects.create(name="Pop")
        self.artist = Artist.objects.create(name="Pipz")
        self.song = Song.objects.create(
            name="Music",
            audio_path="Test.mp3",
            genre_id=self.genre.id,
            artist_id=self.artist.id
        )
        pass

    def test_music_can_get_a_valid_song(self):
        response = client.get(
            reverse('song_details', kwargs={'pk': self.song.id}),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_music_can_get_an_invalid_song(self):
        response = client.get(
            reverse('song_details', kwargs={'pk': 100}),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
