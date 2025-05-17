from django.urls import path
from .views import research_page

urlpatterns = [
    path('', research_page, name='research'),
]
