from django.db import models
from cafesearch.models import Cafe
from django.contrib.auth.models import User # 如果你想關聯到使用者

# Create your models here.
class CafeComment(models.Model):
    cafe_profile = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.FloatField(null=True, blank=True)
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} on {self.cafe.name} at {self.created_at}"