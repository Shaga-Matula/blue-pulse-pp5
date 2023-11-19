# Music App Urls
from django.urls import path

from .views import SongCreateView, SongListView, SongUpdateView, SongDeleteView
from .views import SongListCommentView


urlpatterns = [
    path("song_list", SongListView.as_view(), name="song_list"),
    path("song_create/", SongCreateView.as_view(), name="song_create"),
    path("song_update/<int:pk>/", SongUpdateView.as_view(), name="song_update"),
    path("song_delete/<int:pk>/", SongDeleteView.as_view(), name="song_delete"),
    # Comments
    path('song_all_comments/', SongListCommentView.as_view(), name='song_all_comments'),
    
]
