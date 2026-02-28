from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title, self.content

class Comment(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey(User)
    text = models.TextField
    created_at = models.DateTimeField(auto_now_add=True)

# Create your models here.
