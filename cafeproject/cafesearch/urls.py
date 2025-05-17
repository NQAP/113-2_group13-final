from django.urls import path
from .views import research_page

urlpatterns = [
    path('research/', research_page, name='research'),
]
