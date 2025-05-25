from django.urls import path
from . import views

app_name = 'cafedetail'

urlpatterns = [
    path('add/', views.add_new_cafe_view, name='add_newcafe'),
    path('<slug:slug>/', views.cafe_detail_view, name='cafe_detail'),
]