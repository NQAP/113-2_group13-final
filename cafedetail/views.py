from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify
from cafesearch.models import Cafe
from django.conf import settings
import requests
import json
import os
from django.core.files.storage import default_storage

def cafe_detail_view(request, slug):
    cafe = get_object_or_404(Cafe, slug=slug)

    tags_list = []

    context = {
        'cafe': cafe,
        'tags_list': tags_list,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
    }
    return render(request, 'cafe_detail.html', context) 

def add_new_cafe_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        booking_url = request.POST.get('booking_url')
        uploaded_image_file = request.FILES.get('image') # <-- 從 request.FILES 獲取上傳的圖片檔案
        features = request.POST.getlist('features') 
        min_spending = request.POST.get('min_spending')
        rating = request.POST.get('rating')

        # --- 1. 獲取經緯度 ---
        latitude = None
        longitude = None
        if address and hasattr(settings, 'GOOGLE_MAPS_API_KEY') and settings.GOOGLE_MAPS_API_KEY:
            geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={settings.GOOGLE_MAPS_API_KEY}"
            try:
                response = requests.get(geocode_url)
                data = response.json()
                if data['status'] == 'OK' and data['results']:
                    location = data['results'][0]['geometry']['location']
                    latitude = location['lat']
                    longitude = location['lng']
                else:
                    print(f"Geocoding failed for address: {address}. Status: {data.get('status')}")
            except requests.exceptions.RequestException as e:
                print(f"Geocoding API request failed: {e}")
            except (KeyError, IndexError) as e:
                print(f"Error parsing Geocoding API response: {e}")
        else:
            print("地址為空或 Google Maps API 金鑰未配置。")


        # --- 2. 處理圖片上傳並組裝 URL ---
        image_url_to_save = None
        if uploaded_image_file:
            # 定義儲存路徑，例如 'cafe_images/檔案名稱.jpg'
            # 確保 cafe_images 這個子資料夾在 media/ 下是存在的 (Django 會自動創建)
            file_name = default_storage.save(os.path.join('cafe_images', uploaded_image_file.name), uploaded_image_file)
            
            # 例如：/media/cafe_images/my_uploaded_image.jpg
            image_url_to_save = settings.MEDIA_URL + file_name 

        # --- 3. 生成 slug ---
        cafe_slug = slugify(name)
        # 檢查 slug 是否已經存在，如果存在則加一個數字後綴
        original_slug = cafe_slug
        counter = 1
        while Cafe.objects.filter(slug=cafe_slug).exists():
            cafe_slug = f"{original_slug}-{counter}"
            counter += 1

        # --- 4. 創建 Cafe 物件並儲存 ---
        try:
            new_cafe = Cafe.objects.create(
                name=name,
                address=address,
                latitude=latitude,
                longitude=longitude,
                booking_url=booking_url,
                image_url=image_url_to_save, # <-- 將組裝好的 URL 儲存到 image_url
                tags=features, 
                min_spending=int(min_spending) if min_spending else None, 
                rating=float(rating) if rating else None, 
                slug=cafe_slug,
            )
            return redirect('cafedetail:cafe_detail', slug=new_cafe.slug)

        except Exception as e:
            print(f"Error saving cafe: {e}")
            context = {'error': f'新增咖啡廳失敗：{e}，請檢查輸入資訊。',
                       'name': name, 'address': address, 'booking_url': booking_url,
                       'features': features, 'min_spending': min_spending,}
            return render(request, 'add_newcafe.html', context)

    return render(request, 'add_newcafe.html', {})