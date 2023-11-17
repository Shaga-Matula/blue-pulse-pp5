# Music App Urls


from django.urls import path
from . import views


urlpatterns = [
    path("song_list", views.SongListView.as_view(), name="song_list"),
    
] 