from django.db import models
from django.contrib.auth.models import AbstractUser

class Account(AbstractUser):
    """
    Base authentication model for both admins and teams.
    Teams will share a single account.
    
    Note: password field is inherited from AbstractUser, no need to define it explicitly.
    Authentication is handled at the Account level, not the TeamProfile level.
    """
    is_admin = models.BooleanField(default=False)
    # No need for a is_team flag - anything that's not an admin is a team account


class TeamProfile(models.Model):
    """
    Additional information about a team.
    Each team has one shared Account for login.
    """
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='team')
    team_name = models.CharField(max_length=100)  # Display name for the team
    score = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-score']
        
    def __str__(self):
        return self.team_name


class TeamMember(models.Model):
    """
    Individual members who are part of a team.
    Teams share login credentials, but we track individual members.
    """
    team = models.ForeignKey(TeamProfile, on_delete=models.CASCADE, related_name='members')
    name = models.CharField(max_length=100)
    joined_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.team.team_name})"


