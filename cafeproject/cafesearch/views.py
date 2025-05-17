from django.shortcuts import render

# Create your views here.
def research_page(request):
    return render(request, 'research.html')