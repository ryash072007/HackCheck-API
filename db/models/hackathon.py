from datetime import timedelta
from django.core.exceptions import ValidationError
from django.db import models
from .question import Question
from .user import TeamMember, TeamProfile


class HackathonSettings(models.Model):
    max_team_size = models.PositiveIntegerField(default=4)
    duration = models.DurationField(default=timedelta(hours=3))

    has_started = models.BooleanField(default=False)
    has_ended = models.BooleanField(default=False)
    is_paused = models.BooleanField(default=False)

    time_started = models.DateTimeField(null=True, blank=True)
    time_ended = models.DateTimeField(null=True, blank=True)
    time_paused = models.DateTimeField(null=True, blank=True)
    time_spent_paused = models.DurationField(default=timedelta(0))

    score_decrement_per_interval = models.IntegerField(default=10)
    score_decrement_interval = models.DurationField(default=timedelta(minutes=10))

    max_score = models.IntegerField(default=300)

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


class ParticipantActivity(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="participant_activities"
    )
    team_member = models.ForeignKey(
        TeamMember, on_delete=models.CASCADE, related_name="participant_activities"
    )
    team = models.ForeignKey(
        TeamProfile, on_delete=models.CASCADE, related_name="participant_activities"
    )
    activity_type = models.CharField(max_length=256)
    details = models.TextField()

    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.team_member} - {self.activity_type} - {self.timestamp}"
