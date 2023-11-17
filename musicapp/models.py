from django.db import models
from cloudinary.models import CloudinaryField


class MusicMod(models.Model):
    artist_name = models.CharField(max_length=100, verbose_name='Artist Name')
    song_title = models.CharField(max_length=100, verbose_name='Song Title')
    song_file = CloudinaryField('song_file', resource_type='auto')
    song_image = CloudinaryField('song_image', default='placeholder')

    def __str__(self):
        return f"{self.artist_name} - {self.song_title}"