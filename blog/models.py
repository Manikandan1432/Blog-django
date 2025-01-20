from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Datas(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    img_url = models.URLField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=False, null=False)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title
class AboutUs(models.Model):
    content = models.TextField()