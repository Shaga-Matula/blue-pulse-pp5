from django.urls import path
from .views import SubscribeSuccessView, SubscribeView

urlpatterns = [
    path('subscribe/', SubscribeView.as_view(), name='subscribe'),
    path('subscribe/success/', SubscribeSuccessView.as_view(), name='subscribe_success'),
]