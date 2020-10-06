from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    pass

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="userMessages")
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.message}"

    def serialize(self):
        return {
            "user": self.user,
            "message": self.message,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        }