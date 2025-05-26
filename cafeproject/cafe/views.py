from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from cafesearch.models import Cafe

from django.conf import settings


def index(request):
    cafes = Cafe.objects.all()
    districts = Cafe.objects.values_list('district', flat=True).distinct()
    if request.method == 'POST':
        cafes = Cafe.objects.all()
        districts = Cafe.objects.values_list('district', flat=True).distinct()
        filters = []
        district = request.POST.get('district')
        unlimited_time = request.POST.get('unlimited_time')
        has_socket = request.POST.get('has_socket')
        has_meal = request.POST.get('has_meal')
        quiet = request.POST.get('quiet')
        pet_friendly = request.POST.get('pet_friendly')
        min_spending_min = request.POST.get('min_spending_min')
        min_spending_max = request.POST.get('min_spending_max')
        rating = request.POST.get('rating')
        if not district:
            district = '不限'
        if unlimited_time:
            filters.append('unlimited_time')
        if has_socket:
            filters.append('has_socket')
        if has_meal:
            filters.append('has_meal')
        if quiet:
            filters.append('quiet')
        if pet_friendly:
            filters.append('pet_friendly')
        context = {
            'filters': filters,
            'min_spending_min': min_spending_min,
            'min_spending_max': min_spending_max,
            'rating': rating,
        }
        print(context)
        return render(request, 'research.html', {
            'cafes': cafes,
            'districts': sorted(set(districts)),
            'google_api_key': settings.GOOGLE_MAPS_API_KEY,
            'filters': filters,
            'min_spending_min': min_spending_min,
            'min_spending_max': min_spending_max,
            'rating': rating,
            'district': district,
        })

    return render(request, 'index.html', {
        'cafes': cafes,
        'districts': sorted(set(districts)),
        'google_api_key': settings.GOOGLE_MAPS_API_KEY
    })

# Create your views here.
class ProtectedView(APIView):
  permission_classes = [IsAuthenticated]
  
  def get(self, request):
    return Response({
      "message": "您已通過認證",
      "user_id": request.user.id,
      "username": request.user.username
    })

class LogoutView(APIView):
  permission_classes = [IsAuthenticated]
  
  def post(self, request):
    try:
      refresh_token = request.data.get("refresh")
      if not refresh_token:
        return Response({"error": "Refresh token is required"}, status=400)
        
      token = RefreshToken(refresh_token)
      token.blacklist()
      
      return Response({
        "success": True,
        "message": "您已成功登出",
        "status": "Token has been blacklisted successfully"
      })
    except Exception as e:
      return Response({
        "success": False,
        "error": str(e),
        "message": "登出時發生錯誤"
      }, status=400)

def register_page(request):
	return render(request, 'register.html')

@method_decorator(csrf_exempt, name='dispatch')
class RegisterAPI(APIView):
	def post(self, request):
		try:
			data = request.data
			username = data.get("username")
			password = data.get("password")

			if not username or not password:
				return JsonResponse({"error": "缺少帳號或密碼"}, status=400)

			if User.objects.filter(username=username).exists():
				return JsonResponse({"error": "帳號已存在"}, status=400)

			User.objects.create_user(username=username, password=password)
			return JsonResponse({"message": "註冊成功"})
		except Exception as e:
			return JsonResponse({"error": str(e)}, status=400)
          

