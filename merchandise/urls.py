from django.urls import path
from .views import AllMerchView, MerchandiseDetailView
from . import views


urlpatterns = [
    path('all_merchandise/', AllMerchView.as_view(), name='all_merchandise'),
    path('all_merchandise/<int:pk>/', MerchandiseDetailView.as_view(), name='merch_item'),
    path('add/', views.add_merch, name='add_merch')
]
