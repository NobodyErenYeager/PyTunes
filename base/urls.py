from django.urls import path
from .views import (
    AlbumListCreateAPIView, AlbumRetrieveUpdateDestroyAPIView,
    SongListCreateAPIView, SongRetrieveUpdateDestroyAPIView,
    PlaylistListCreateAPIView, PlaylistRetrieveUpdateDestroyAPIView
)
from . import views


urlpatterns = [
    # ///////////////////////// View Endpoints ///////////////////////////
    path('', views.home, name='home'),
    path('album/<int:album_id>/', views.album_detail, name='album'),
    path('album/<int:album_id>/edit/', views.edit_album, name='edit-album'),
    path('album/<int:album_id>/favorite/', views.album_fovorite, name='album-favorite'),
    path('song/<int:song_id>/edit/', views.edit_song, name='edit-song'),
    path('song/<int:song_id>/favorite/', views.song_favorite, name='song-favorite'),
    path('albums/', views.album_list, name='album-list'),
    path('songs/', views.song_list, name='song-list'),
    path('favorites/', views.favorite_list, name='favorite-list'),
    path('song/<int:song_id>/playlists/', views.update_song_playlists, name='update-song-playlists'),
    path('playlists/', views.playlist_list, name='playlist-list'),
    path('playlists/create/', views.create_playlist, name='create-playlist'),
    path('playlists/<int:playlist_id>/', views.playlist_detail, name='playlist'),
    path('playlists/<int:playlist_id>/delete/', views.delete_playlist, name='delete-playlist'),
    path('playlist/<int:playlist_id>/add-songs/', views.playlist_add_songs, name='playlist-add-songs'),
    path('songs/download/', views.download_song_list, name='download-songs'),
    path('player/', views.player, name='player'),
    path('storage-service/', views.storage_service_list, name="storage_service_list"),
    path('storage-service/add/', views.add_storage_service, name="add_storage_service"),
    path('storage-service/edit/<int:service_id>/', views.edit_storage_service, name="edit_storage_service"),
    path('storage-service/add-link/<int:album_id>/', views.add_storage_link, name="add_storage_link"),
    path('storage-service/edit-link/<int:link_id>/', views.edit_storage_link, name="edit_storage_link"),
    path('storage-service/delete-link/<int:link_id>/', views.delete_storage_link, name="delete_storage_link"),

    # /////////////////////////// API Endpoints ///////////////////////
    path('api/albums/', AlbumListCreateAPIView.as_view(), name='album-list-create'),
    path('api/albums/<int:pk>/', AlbumRetrieveUpdateDestroyAPIView.as_view(), name='album-detail'),
    path('api/songs/', SongListCreateAPIView.as_view(), name='song-list-create'),
    path('api/songs/<int:pk>/', SongRetrieveUpdateDestroyAPIView.as_view(), name='song-detail'),
    path('api/playlists/', PlaylistListCreateAPIView.as_view(), name='playlist-list-create'),
    path('api/playlists/<int:pk>/', PlaylistRetrieveUpdateDestroyAPIView.as_view(), name='playlist-detail'),
]
