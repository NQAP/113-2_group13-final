from django.shortcuts import render, get_object_or_404
from .models import Cafe
from django.conf import settings


def search_page(request):
    cafes = Cafe.objects.all()
    return render(request, 'research.html', {
        'cafes': cafes,
        'google_api_key': settings.GOOGLE_MAPS_API_KEY
    })

def cafe_detail(request, slug):
    cafe = get_object_or_404(Cafe, slug=slug)
    return render(request, 'cafe_detail.html', {'cafe': cafe})
