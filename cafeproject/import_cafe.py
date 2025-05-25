import os
import django
import pandas as pd
from django.utils.text import slugify

# 設定 Django 環境
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cafeproject.settings")
django.setup()

from cafesearch.models import Cafe

# 讀取 Excel 檔案
file_path = "min_max_不限時咖啡廳.xlsx"
df = pd.read_excel(file_path)

# 將 NaN 轉為 None
df = df.where(pd.notnull(df), None)

def clean_tags(tag_string):
	if not tag_string:
		return []
	# 先用逗號分割，再 strip 空白與引號
	return [tag.strip().strip('"').strip("'") for tag in tag_string.split(',')]

# 寫入資料庫
for _, row in df.iterrows():
	cafe, created = Cafe.objects.get_or_create(
		slug=slugify(row["slug"])[:50],
		defaults={
			"name": row["name"],
			"address": row["address"],
			"district": row["district"],
			"image_url": row["image_url"],
			"tags": clean_tags(row["tags"]),
			"rating": row["rating"],
			"min_spending_min": int(row["min_spending_min"]) if not pd.isna(row["min_spending_min"]) else None,
			"min_spending_max": int(row["min_spending_max"]) if not pd.isna(row["min_spending_max"]) else None,
		}
	)
	if created:
		print(f"✅ 新增：{cafe.name}")
	else:
		print(f"⚠️ 已存在：{cafe.name}，略過匯入")
