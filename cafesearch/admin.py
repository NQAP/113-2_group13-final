from django.contrib import admin
from .models import Cafe


@admin.register(Cafe)
class CafeAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'slug']
    
    def address(self, obj):
        address_parts = [
            obj.city, obj.district, obj.street_name,
            f"{obj.lane}巷" if obj.lane else "",
            f"{obj.alley}弄" if obj.alley else "",
            f"{obj.number}號" if obj.number else "",
            f"{obj.floor}樓" if obj.floor else "",
            f"{obj.room}室" if obj.room else "",
        ]
        return " ".join(filter(None, address_parts))

    address.short_description = '地址'
