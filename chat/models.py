from django.db import models
from django.contrib.auth.models import User
class Room(models.Model):
    name = models.CharField(max_length=200,unique=True)

    def __str__(self) -> str:
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    content = models.TextField()
    timestamp =models.TimeField(auto_now_add=True)
    created_at =models.TimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user}:{self.room}: {self.content[:20]}'
    class Meta:
        ordering = ['-timestamp']