from django.db import models
from django.db.models.deletion import CASCADE
from rareapi.models.post import Post
from rareapi.models.rareuser import RareUser


class Comment(models.Model):
    content = models.CharField(max_length=250)
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=CASCADE, related_name='comments')
    author = models.ForeignKey(RareUser, on_delete=CASCADE, related_name='comments')