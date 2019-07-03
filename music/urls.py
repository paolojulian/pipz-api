#music/urls.py

from django.urls import include, re_path

from .views import CreateGenre
from .views import GenreDetails
from .views import CreateArtist
from .views import ArtistDetails
from .views import CreateSong
from .views import SongDetails

urlpatterns = [

    # POST - create genre, GET - get all genre
    re_path(r'^genre/$', CreateGenre.as_view(), name='genre'),
    # PUT, DELETE, GET
    re_path(r'^genre/(?P<pk>[0-9]+)/$', GenreDetails.as_view(), name='genre_details'),

    # POST - create artist, GET - get all artists
    re_path(r'^artist/$', CreateArtist.as_view(), name='artist'),
    # PUT, DELETE, GET
    re_path(r'^artist/(?P<pk>[0-9]+)/$', ArtistDetails.as_view(), name='artist_details'),

    # POST - create a song, GET - get all songs
    re_path(r'^song/$', CreateSong.as_view(), name='song'),
    # PUT, DELETE, GET
    re_path(r'^song/(?P<pk>[0-9]+)/$', SongDetails.as_view(), name='song_details'),
]
