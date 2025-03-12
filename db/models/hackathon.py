from datetime import timedelta
from django.core.exceptions import ValidationError
from django.db import models

class HackathonSettings(models.Model):
    max_team_size = models.PositiveIntegerField(default=4)
    duration = models.DurationField(default=timedelta(hours=3))

    has_started = models.BooleanField(default=False)
    has_ended = models.BooleanField(default=False)
    is_paused = models.BooleanField(default=False)
    
    time_started = models.DateTimeField(null=True, blank=True)
    time_ended = models.DateTimeField(null=True, blank=True)
    time_paused = models.DateTimeField(null=True, blank=True)
    time_resumed = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Hackathon Settings"
    
    def save(self, *args, **kwargs):
        if HackathonSettings.objects.exists() and not self.pk:
            raise ValidationError("Only one instance of HackathonSettings can exist")
        return super().save(*args, **kwargs)
    
    @classmethod
    def get_instance(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
    
    def __str__(self):
        return f"Max Team Size: {self.max_team_size}, Duration: {self.duration}"
