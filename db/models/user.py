from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    team = models.ForeignKey('Team', on_delete=models.SET_NULL, null=True, related_name='members')

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    score = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-score']  # For leaderboard sorting


