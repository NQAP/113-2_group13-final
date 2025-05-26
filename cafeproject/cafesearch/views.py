from django.shortcuts import render, get_object_or_404, redirect
from .models import Cafe
from django.conf import settings


def search_page(request):
    cafes = Cafe.objects.all()
    districts = Cafe.objects.values_list('district', flat=True).distinct()
    return render(request, 'research.html', {
        'cafes': cafes,
        'districts': sorted(set(districts)),
        'google_api_key': settings.GOOGLE_MAPS_API_KEY,
        'filters': [],
        'min_spending_min': '不限',
        'min_spending_max': '不限',
        'rating': '不限',
        'district': '不限',
    })

def cafe_detail(request, slug):
    return redirect(f'/cafedetail/{slug}')
