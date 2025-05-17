from django.db import models
from django.urls import reverse

class Cafe(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    image_url = models.URLField()
    slug = models.SlugField(unique=True)
    tags = models.JSONField(default=list)

    @property
    def detail_url(self):
        return reverse('cafe-detail', kwargs={'slug': self.slug})

