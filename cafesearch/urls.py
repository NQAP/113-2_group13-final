from django.urls import path
from .views import research_page, cafe_detail

urlpatterns = [
    path('research/', research_page, name='research'),
    path('<slug:slug>/', cafe_detail, name='cafe-detail'),
]