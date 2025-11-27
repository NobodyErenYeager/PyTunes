from django.forms import ModelForm
from .models import (
    Album, Song, Playlist, StorageService, StorageLink, 
    Podcast, PodcastEpisode, PodcastStorageLink,
    AudioBook, AudioBookChapter, AudioBookStorageLink
)


class AlbumForm(ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'album_image', 'favorite']

    def __init__(self, *args, **kwargs):
        super(AlbumForm, self).__init__(*args, **kwargs)
        self.fields['album_image'].widget.attrs.update({'rows': '1'})


class SongForm(ModelForm):
    class Meta:
        model = Song
        fields = ['album', 'title', 'single_image', 'artist', 'favorite', 'play_url']

    def __init__(self, *args, **kwargs):
        super(SongForm, self).__init__(*args, **kwargs)
        self.fields['single_image'].widget.attrs.update({'rows': '1'})
        self.fields['artist'].widget.attrs.update({'rows': '1'})
        self.fields['play_url'].widget.attrs.update({'rows': '1'})


class PlaylistForm(ModelForm):
    class Meta:
        model = Playlist
        fields = ['title']


class StorageServiceForm(ModelForm):
    class Meta:
        model = StorageService
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(StorageServiceForm, self).__init__(*args, **kwargs)
        self.fields['url'].widget.attrs.update({'rows': 1})
        self.fields['icon'].widget.attrs.update({'rows': 1})


class StorageLinkForm(ModelForm):
    class Meta:
        model = StorageLink
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super(StorageLinkForm, self).__init__(*args, **kwargs)
        self.fields['link'].widget.attrs.update({'rows': 1})
