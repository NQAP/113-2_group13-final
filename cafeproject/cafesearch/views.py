from django.shortcuts import render, get_object_or_404
from .models import Cafe

def research_page(request):
    cafes = Cafe.objects.all()
    return render(request, 'research.html', {"cafes": cafes})

def cafe_detail(request, slug):
    cafe = get_object_or_404(Cafe, slug=slug)
    return render(request, 'cafe_detail.html', {'cafe': cafe})