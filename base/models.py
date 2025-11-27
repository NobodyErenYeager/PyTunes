from django.db import models


class Album(models.Model):
    title = models.CharField(max_length=2000)
    album_image = models.TextField(null=True, blank=True)
    favorite = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}"


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True, related_name='songs')
    title = models.CharField(max_length=2000)
    message_id = models.IntegerField()
    channel_id = models.IntegerField()
    file_name = models.CharField(max_length=2000)
    single_image = models.TextField(null=True, blank=True)
    artist = models.TextField(null=True, blank=True)
    favorite = models.BooleanField(default=False)
    play_url = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.title}"


class Playlist(models.Model):
    title = models.CharField(max_length=2000)
    songs = models.ManyToManyField(Song, related_name='playlists', null=True, blank=True)

    def __str__(self):
        return self.title


class StorageService(models.Model):
    name = models.CharField(max_length=1000)
    url = models.TextField(null=True, blank=True)
    icon = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class StorageLink(models.Model):
    service = models.ForeignKey(StorageService, on_delete=models.CASCADE, related_name='links')
    link = models.TextField()
    note = models.CharField(max_length=500, null=True, blank=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='storage_links')

    def __str__(self):
        return f"{self.album.title} - {self.service.name}"


class Podcast(models.Model):
    title = models.CharField(max_length=5000)
    feed_url = models.TextField()
    podcast_image = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class PodcastEpisode(models.Model):
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE, related_name='episodes')
    title = models.TextField()
    description = models.TextField(null=True, blank=True)
    episode_image = models.TextField(null=True, blank=True)
    audio_url = models.TextField()
    downloaded_url = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.podcast.title} - {self.title}"
    

class PodcastStorageLink(models.Model):
    service = models.ForeignKey(StorageService, on_delete=models.CASCADE, related_name='podcast_links')
    link = models.TextField()
    note = models.CharField(max_length=500, null=True, blank=True)
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE, related_name='storage_links')

    def __str__(self):
        return f"{self.podcast.title} - {self.service.name}"
    

class AudioBook(models.Model):
    title = models.CharField(max_length=10000)
    # author = models.CharField(max_length=2000, null=True, blank=True)
    book_image = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
    

class AudioBookChapter(models.Model):
    audiobook = models.ForeignKey(AudioBook, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=10000)
    note = models.CharField(max_length=500, null=True, blank=True)
    file_url = models.TextField()

    def __str__(self):
        return f"{self.audiobook.title} - {self.title}"
    

class AudioBookStorageLink(models.Model):
    service = models.ForeignKey(StorageService, on_delete=models.CASCADE, related_name='audiobook_links')
    link = models.TextField()
    audiobook = models.ForeignKey(AudioBook, on_delete=models.CASCADE, related_name='storage_links')

    def __str__(self):
        return f"{self.audiobook.title} - {self.service.name}"
