from django.shortcuts import render, redirect
from rest_framework import generics
from .models import (
    Album, Song, Playlist, StorageService, StorageLink, 
    Podcast, PodcastEpisode, PodcastStorageLink,
    AudioBook, AudioBookChapter, AudioBookStorageLink
)
from .serializers import AlbumSerializer, SongSerializer, PlaylistSerializer
from django.db.models import Value, CharField
from . import forms
from django.urls import reverse
from django.http import JsonResponse
from django.db.models.functions import Lower
from django.db.models import Q
import json


# ///////////////////////// Views ///////////////////////////
def home(request):
    albums = Album.objects.all().order_by(Lower('title'))
    # songs = Song.objects.filter(album=None)

    # items = list(albums.values('id', 'title', 'album_image', 'favorite').annotate(type=Value('album', output_field=CharField())))
    # items += list(songs.values('id', 'title', 'single_image', 'artist', 'favorite').annotate(type=Value('song', output_field=CharField())))
    # sorted_items = sorted(items, key=lambda x: x['title'].lower())

    # for album in albums:
    #     for song in album.songs.all():
    #         song.single_image = album.album_image
    #         song.save()

    return render(request, 'home.html', {'items': albums, 'page_title': 'Albums'})


def album_detail(request, album_id):
    try:
        album = Album.objects.get(id=album_id)
    except Album.DoesNotExist:
        pass
    return render(request, 'album_detail.html', {'album': album})


def edit_album(request, album_id):
    # referer = request.META.get('HTTP_REFERER', '/')
    try:
        album = Album.objects.get(id=album_id)
    except Album.DoesNotExist:
        return redirect('album', album_id=album_id)
    form = forms.AlbumForm(instance=album)
    if request.method == 'POST':
        form = forms.AlbumForm(request.POST, request.FILES, instance=album)
        if form.is_valid():
            album_form = form.save(commit=False)
            if album_form.album_image:
                for song in album.songs.all():
                    song.single_image = album_form.album_image
                    song.save()
            album_form.save()
            return redirect('album', album_id=album_id)
    context = {
        'form': form,
        'form_title': 'Edit Album'
    }
    return render(request, 'form.html', context)


def album_fovorite(request, album_id):
    try:
        album = Album.objects.get(id=album_id)
        album.favorite = not album.favorite
        album.save()
    except Album.DoesNotExist:
        pass
    return redirect('album', album_id=album_id)


def edit_song(request, song_id):
    try:
        song = Song.objects.get(id=song_id)
    except Song.DoesNotExist:
        return redirect('home')

    if request.method == 'GET':
        referer = request.META.get('HTTP_REFERER')
        if referer:
            request.session['prev_page'] = referer

    form = forms.SongForm(request.POST or None, request.FILES or None, instance=song)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(request.session.pop('prev_page', reverse('home')))

    context = {
        'form': form,
        'form_title': 'Edit Song',
    }
    return render(request, 'form.html', context)


def song_favorite(request, song_id):
    try:
        song = Song.objects.get(id=song_id)
        song.favorite = not song.favorite
        song.save()
    except Song.DoesNotExist:
        pass
    return redirect(request.META.get('HTTP_REFERER', reverse('home')))


def album_list(request):
    albums = Album.objects.all().order_by(Lower('title'))
    return render(request, 'home.html', {'items': albums, 'page_title': 'Albums'})


def song_list(request):
    songs = Song.objects.all().order_by(Lower('title'))
    return render(request, 'songs.html', {'songs': songs, 'page_title': 'Songs', 'type': 'song'})


def favorite_list(request):
    songs = Song.objects.filter(favorite=True).order_by(Lower('title'))
    return render(request, 'songs.html', {'songs': songs, 'page_title': 'Favorite Songs', 'type': 'favorite'})


def update_song_playlists(request, song_id):
    song = Song.objects.get(id=song_id)
    if not song:
        return redirect('song-list')
    playlists = Playlist.objects.all()

    if request.method == 'POST':
        selected_ids = request.POST.getlist('playlists')
        selected_playlists = Playlist.objects.filter(id__in=selected_ids)
        song.playlists.set(selected_playlists)
        return redirect(request.GET.get('next','home'))

    return render(request, 'add_to_playlist.html', {
        'song': song,
        'playlists': playlists,
        'form_title': f'Add "{song.title}" to Playlists'
    })


def create_playlist(request):
    form = forms.PlaylistForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        playlist = form.save()
        return redirect('playlist-list')

    context = {
        'form': form,
        'form_title': 'Create Playlist',
    }
    return render(request, 'form.html', context)


def playlist_list(request):
    playlists = Playlist.objects.all().order_by(Lower('title'))
    return render(request, 'playlists.html', {'playlists': playlists})


def playlist_detail(request, playlist_id):
    try:
        playlist = Playlist.objects.get(id=playlist_id)
    except Playlist.DoesNotExist:
        return redirect('playlist-list')

    songs = playlist.songs.all()
    return render(request, 'songs.html', {
        'playlist': playlist,
        'songs': songs,
        'page_title': playlist.title,
        'type': 'playlist'
    })


def delete_playlist(request, playlist_id):
    try:
        playlist = Playlist.objects.get(id=playlist_id)
        playlist.delete()
    except Playlist.DoesNotExist:
        pass
    return redirect('playlist-list')


def playlist_add_songs(request, playlist_id):
    try:
        playlist = Playlist.objects.get(id=playlist_id)
    except Playlist.DoesNotExist:
        return redirect('playlist-list')
    all_songs = Song.objects.all()

    if request.method == 'POST':
        selected_song_ids = request.POST.getlist('songs')
        playlist.songs.set(selected_song_ids)
        return redirect('playlist', playlist_id=playlist.id)

    context = {
        'playlist': playlist,
        'all_songs': all_songs,
    }
    return render(request, 'playlist_add_songs.html', context)


def download_song_list(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('songs')
        songs = Song.objects.filter(id__in=selected_ids).select_related('album')
        data = [
            {
                'id': song.id,
                'title': song.title,
                'file_name': song.file_name,
                'album': {"title": song.album.title, "album_image": song.album.album_image} if song.album else None,
                'message_id': song.message_id,
                'channel_id': song.channel_id,
                'single_image': song.single_image,
                'artist': song.artist,
            }
            for song in songs
        ]
        return JsonResponse(data, safe=False)

    all_songs = Song.objects.all().order_by('-id')
    return render(request, 'song_download_list.html', {'songs': all_songs})


def player(request):
    songs = Song.objects.filter(~Q(play_url=None)).order_by(Lower('title'))
    default_play_queue = [{"title": song.title, "image": song.single_image, "url": song.play_url} for song in songs]
    # print(default_play_queue)
    return render(request, 'player.html', {'songs': songs, 'default_play_queue': json.dumps(default_play_queue)})


def storage_service_list(request):
    storage_services = StorageService.objects.all()
    return render(request, 'storage_services.html', {'storage_services': storage_services})


def add_storage_service(request):
    form = forms.StorageServiceForm()
    if request.method == "POST":
        form = forms.StorageServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('storage_service_list')
    context = {
        "form": form,
        "form_title": "Add Storage Service"
    }
    return render(request, 'form.html', context)


def edit_storage_service(request, service_id):
    service = StorageService.objects.get(id=service_id)
    form = forms.StorageServiceForm(instance=service)
    if request.method == "POST":
        form = forms.StorageServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('storage_service_list')
    context = {
        "form": form,
        "form_title": "Edit Storage Service"
    }
    return render(request, 'form.html', context)


def add_storage_link(request, album_id):
    try:
        album = Album.objects.get(id=album_id)
    except Album.DoesNotExist:
        return redirect('home')
    form = forms.StorageLinkForm(initial={"album": album})
    if request.method == "POST":
        form = forms.StorageLinkForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('album', album_id)
    context = {
        "form": form,
        "form_title": "Add Link"
    }
    return render(request, 'form.html', context)


def edit_storage_link(request, link_id):
    try:
        link = StorageLink.objects.get(id=link_id)
    except StorageLink.DoesNotExist:
        return redirect('home')
    form = forms.StorageLinkForm(instance=link)
    if request.method == "POST":
        form = forms.StorageLinkForm(request.POST, instance=link)
        if form.is_valid():
            form.save()
            return redirect('album', link.album.id)
    
    context = {
        'form': form,
        'form_page': "Edit Link"
    }
    return render(request, 'form.html', context)


def delete_storage_link(request, link_id):
    try:
        link = StorageLink.objects.get(id=link_id)
    except StorageLink.DoesNotExist:
        return redirect('home')
    
    album_id = link.album.id
    link.delete()
    return redirect('album', album_id)

# /////////////////////////// API Views ///////////////////////////
# Album Views
class AlbumListCreateAPIView(generics.ListCreateAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

class AlbumRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

# Song Views
class SongListCreateAPIView(generics.ListCreateAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

class SongRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

# Playlist Views
class PlaylistListCreateAPIView(generics.ListCreateAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

class PlaylistRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
