from django.db import models
from django.db.models.deletion import CASCADE
from .category import Category
from .rareuser import RareUser


class Post(models.Model):
    author = models.ForeignKey(RareUser, on_delete=CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=CASCADE, related_name='posts')
    title = models.CharField(max_length=100)
    publication_date = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField()
    content = models.TextField()
    # CharField: chunk of space, not flexible, faster when smaller; 
    # TextField: rows can be smaller, no attribute
    approved = models.BooleanField(default=False)
    