import requests
from django.conf import settings
from django.db import models
from django.urls import reverse


class Cafe(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    district = models.CharField(max_length=20, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    image_url = models.CharField(max_length=500)
    slug = models.SlugField(unique=True)
    tags = models.JSONField(null=True, blank=True, default=list)
    rating = models.FloatField(null=True, blank=True)
    min_spending_min = models.IntegerField(null=True, blank=True)
    min_spending_max = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # 如果還沒填緯度和經度，就從地址查詢
        if (not self.latitude or not self.longitude) and self.address:
            lat, lng = self.geocode_address()
            if lat and lng:
                self.latitude = lat
                self.longitude = lng
        super().save(*args, **kwargs)

    def geocode_address(self):
        api_key = settings.GOOGLE_MAPS_API_KEY
        response = requests.get(
            "https://maps.googleapis.com/maps/api/geocode/json",
            params={"address": self.address, "key": api_key}
        )
        results = response.json().get("results")
        if results:
            location = results[0]["geometry"]["location"]
            return location["lat"], location["lng"]
        return None, None

    @property
    def detail_url(self):
        return reverse('cafe-detail', kwargs={'slug': self.slug})


# 登入、註冊
class Tag(models.Model):
    status = models.CharField(max_length=50, null=False)
    def __str__(self):
        return self.status

class Post(models.Model):
    tags = models.ForeignKey('Tag', on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50, null=False, default='請填寫暱稱')
    cafe = models.CharField(max_length=50, null=False, default='請填寫咖啡廳名稱')
    address = models.TextField(max_length=50, null=False, default='請填寫地址')
    cafe_url = models.URLField(null=True, default='請填寫訂位網站連結')
    del_pass = models.CharField(max_length=50)
    pub_time = models.DateTimeField(auto_now=True)
    enabled = models.BooleanField(default=False) #改True就可以預設為開啟
    def __str__(self):
        return self.cafe
    
class User(models.Model):
    name = models.CharField(max_length=20, null=False)
    email = models.EmailField()
    password = models.CharField(max_length=20, null=False)
    enabled = models.BooleanField(default=False)
    def __str__(self):
        return self.name

