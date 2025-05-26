from django.urls import path
from .views import search_page, cafe_detail

urlpatterns = [
    path('', search_page, name='research'),
    path('<slug:slug>/', cafe_detail, name='cafe-detail'),
]
