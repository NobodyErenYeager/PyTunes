from django.contrib import admin
from .models import (
    Album, Song, Playlist, StorageService, StorageLink, 
    Podcast, PodcastEpisode, PodcastStorageLink,
    AudioBook, AudioBookChapter, AudioBookStorageLink
)


# Register your models here.
admin.site.register(Album)
admin.site.register(Song)
admin.site.register(Playlist)
admin.site.register(StorageService)
admin.site.register(StorageLink)
admin.site.register(Podcast)
admin.site.register(PodcastEpisode)
admin.site.register(PodcastStorageLink)
admin.site.register(AudioBook)
admin.site.register(AudioBookChapter)
admin.site.register(AudioBookStorageLink)
