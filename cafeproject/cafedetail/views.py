from django.shortcuts import render, get_object_or_404, redirect
from slugify import slugify
from django.http import JsonResponse
from cafesearch.models import Cafe
from cafedetail.models import CafeComment
from django.contrib.auth.models import User # 如果你想關聯到使用者
from django.conf import settings
import requests
import json
import os
from django.core.files.storage import default_storage

def cafe_detail_view(request, slug):
    if request.method == 'POST':
        cafe = get_object_or_404(Cafe, slug=slug)
        cafe_element = {
            'name': cafe.name,
            'address': cafe.address,
            'image_url': cafe.image_url,
            'tags_list': cafe.tags,
            'rating': cafe.rating,
        }
        return JsonResponse({'cafe': cafe_element})

    else:
        cafe = get_object_or_404(Cafe, slug=slug)
        tags_list = cafe.tags 
        english_tags_list = ['unlimited_time', 'has_socket', 'has_meal', 'quiet', 'pet_friendly']
        chinese_tags_list = ['不限時', '有插座', '正餐', '安靜', '寵物友善']
        for tag in tags_list:
            if tag in english_tags_list:
                index = english_tags_list.index(tag)
                tags_list[tags_list.index(tag)] = chinese_tags_list[index]
            else:
                continue
        context = {
            'cafe': cafe,
            'tags_list': tags_list,
            'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
        }
        return render(request, 'cafe_detail.html', context)

def add_new_cafe_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        
        city = '台北市'
        district = request.POST.get('district') or None 
        street_name = request.POST.get('street_name') or None
        lane = request.POST.get('lane') or None
        alley = request.POST.get('alley') or None
        number = request.POST.get('number') or None
        floor = request.POST.get('floor') or None
        room = request.POST.get('room') or None

        booking_url = request.POST.get('booking_url')
        uploaded_image_file = request.FILES.get('image')
        features = request.POST.getlist('features') 
        min_spending_min = int(request.POST.get('min_spending_min'))
        min_spending_max = int(request.POST.get('min_spending_max'))
        rating = request.POST.get('rating')

        # --- 新增: 地址重複性檢查 (插入在這裡，在所有數據獲取之後，其他邏輯之前) ---
        address_query_kwargs = {
            'city': city,
            'district': district,
            'street_name': street_name,
            'lane': lane, 
            'alley': alley,
            'number': number,
            'floor': floor,
            'room': room,
        }
        
        # 查詢資料庫中是否有完全匹配的咖啡廳
        existing_cafe = Cafe.objects.filter(**address_query_kwargs).first()

        if existing_cafe:
            # 如果地址已存在，則返回錯誤訊息並顯示原始輸入
            context = {
                'error': f'新增咖啡廳失敗：此地址 "{existing_cafe.get_full_address()}" 已有咖啡廳 "{existing_cafe.name}" 存在。',
                'name': name,
                'district': request.POST.get('district'),
                'street_name': request.POST.get('street_name'),
                'lane': request.POST.get('lane'),
                'alley': request.POST.get('alley'),
                'number': request.POST.get('number'),
                'floor': request.POST.get('floor'),
                'room': request.POST.get('room'),
                'booking_url': booking_url,
                'features': features, 
                'min_spending_min': min_spending_min,
                'min_spending_max': min_spending_max,
                'rating': rating,
            }
            return render(request, 'add_newcafe.html', context)
        if min_spending_max < min_spending_min:
            context = {
                'error': '新增咖啡廳失敗，最低消費不能高於最高消費'
            }
            return render(request, 'add_newcafe.html', context)

        # --- 1. 獲取經緯度 ---
        latitude = None
        longitude = None
        
        full_address_for_geocode = f"{city}{district or ''}{street_name or ''}"
        if lane: 
            full_address_for_geocode += f"{lane}巷"
        if alley: 
            full_address_for_geocode += f"{alley}弄"
        if number: 
            full_address_for_geocode += f"{number}號"
        if floor: 
            full_address_for_geocode += f"{floor}樓"
        if room: 
            full_address_for_geocode += f"{room}室"

        if full_address_for_geocode and hasattr(settings, 'GOOGLE_MAPS_API_KEY') and settings.GOOGLE_MAPS_API_KEY:
            geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={full_address_for_geocode}&key={settings.GOOGLE_MAPS_API_KEY}"
            try:
                response = requests.get(geocode_url)
                data = response.json()
                if data['status'] == 'OK' and data['results']:
                    location = data['results'][0]['geometry']['location']
                    latitude = location['lat']
                    longitude = location['lng']
                else:
                    print(f"Geocoding failed for address: {full_address_for_geocode}. Status: {data.get('status')}")
            except requests.exceptions.RequestException as e:
                print(f"Geocoding API request failed: {e}")
            except (KeyError, IndexError) as e:
                print(f"Error parsing Geocoding API response: {e}")
        else:
            print("地址為空或 Google Maps API 金鑰未配置。")


        # --- 2. 處理圖片上傳並組裝 URL ---
        image_url_to_save = None
        if uploaded_image_file:
            file_name = default_storage.save(os.path.join('cafe_images', uploaded_image_file.name), uploaded_image_file)
            image_url_to_save = settings.MEDIA_URL + file_name 

        # --- 3. 生成 slug ---
        cafe_slug = slugify(name)
        original_slug = cafe_slug
        counter = 1
        while Cafe.objects.filter(slug=cafe_slug).exists():
            cafe_slug = f"{original_slug}-{counter}"
            counter += 1

        # --- 4. 創建 Cafe 物件並儲存 ---
        english_tags_list = ['unlimited_time', 'has_socket', 'has_meal', 'quiet', 'pet_friendly']
        chinese_tags_list = ['不限時', '有插座', '正餐', '安靜', '寵物友善']
        for feature in features:
            index = chinese_tags_list.index(feature)
            features[features.index(feature)] = english_tags_list[index]
        try:
            new_cafe = Cafe.objects.create(
                name=name,
                # --- 保存細分地址欄位 ---
                city=city, 
                district=district,
                address=full_address_for_geocode,
                street_name=street_name,
                lane=lane,
                alley=alley,
                number=number,
                floor=floor,
                room=room,
                latitude=latitude,
                longitude=longitude,
                # booking_url=booking_url,
                image_url=image_url_to_save, # <-- 將組裝好的 URL 儲存到 image_url
                tags=features,
                min_spending_min=min_spending_min,
                min_spending_max=min_spending_min,
                rating=float(rating) if rating else None, 
                slug=cafe_slug,
            )
            return redirect('cafedetail:cafe_detail', slug=new_cafe.slug)

        except Exception as e:
            print(f"Error saving cafe: {e}")
            context = {
                'error': f'新增咖啡廳失敗：{e}，請檢查輸入資訊。',
                'name': name,
                'district': request.POST.get('district'),
                'street_name': request.POST.get('street_name'),
                'lane': request.POST.get('lane'),
                'alley': request.POST.get('alley'),
                'number': request.POST.get('number'),
                'floor': request.POST.get('floor'),
                'room': request.POST.get('room'),
                'booking_url': booking_url,
                'features': features, 
                'min_spending_min': min_spending_min,
                'min_spending_max': min_spending_max,
                'rating': rating,
            }
            return render(request, 'add_newcafe.html', context)

    return render(request, 'add_newcafe.html', {})

def get_cafe_comments_view(request, slug):
    if request.method == 'POST':
        cafe_profile = Cafe.objects.get(slug=slug)
        comments = CafeComment.objects.filter(cafe_profile=cafe_profile).order_by('-created_at')
        comments_data = []
        for comment in comments:
            comments_data.append({
                'user': comment.user.username,
                'rating': comment.rating,
                'comment_text': comment.comment_text,
                'created_at': comment.created_at,
            })

        if len(comments_data) == 0:
            comments_data.append({
                'user': -1,
                'rating': -1,
                'comment_text': "nothing here",
                'created_at': 0,
            })
        return JsonResponse({'comments': comments_data})
    else: 
        return redirect('cafe:homepage')
    
def add_cafe_comment_ajax_view(request, slug):
    cafe_profile = Cafe.objects.get(slug=slug)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user')
            rating = float(data.get('rating'))
            user = User.objects.get(id=user_id)
            comment_text = data.get('text')
            if comment_text:
                comment = CafeComment(cafe_profile=cafe_profile, user=user, rating=rating, comment_text=comment_text)
                comment.save()
                return JsonResponse({'status': 'success', 'message': '評論已發布', 'user': user.username, 'text': comment_text, 'created_at': comment.created_at.isoformat()})
            else:
                return JsonResponse({'status': 'error', 'message': '評論內容不能為空'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': '無效的 JSON'}, status=400)
    else: 
        return redirect('cafe:homepage')