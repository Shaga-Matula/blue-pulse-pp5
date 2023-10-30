
from django.contrib import admin
from django.urls import path
from .views import AllMerchandiseView

urlpatterns = [
    path('all_merchandise/', AllMerchandiseView.as_view(), name='all_merchandise'),
]
