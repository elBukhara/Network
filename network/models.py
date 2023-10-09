from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField('self',blank=True,related_name='user_followers',symmetrical=False)
    following = models.ManyToManyField('self',blank=True,related_name='user_following',symmetrical=False)


class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="author")
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name="likes")

    # I've added serializer for the future 
    def serialize(self):
        return {
            "id": self.id,
            "author": self.user.username,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%m %d %Y, %H:%M"),
        }
    
    def __str__(self):
        return f"Post {self.id}: {self.user}"
