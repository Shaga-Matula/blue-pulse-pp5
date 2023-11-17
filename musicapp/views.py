from django.views.generic import ListView

from .models import MusicMod


class SongListView(ListView):
    model = MusicMod
    template_name = "musicapp/song_list.html"
    context_object_name = "songs"
