import os
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from .user import TeamMember, TeamProfile
import uuid


class Question(models.Model):
    """
    Model to store questions for the quiz.
    """

    title = models.CharField(max_length=300)
    number = models.IntegerField(unique=True, null=False, blank=False)
    description = models.TextField()
    difficulty = models.CharField(
        max_length=10,
        choices=[("easy", "Easy"), ("medium", "Medium"), ("hard", "Hard")],
    )

    samples = models.JSONField(null=True, blank=True)
    tests = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        structure: {
            "input": [],
            "output": []
            }
        """
        if self.samples is not None:
            if not isinstance(self.samples, dict):
                raise ValidationError("Samples must be a dictionary.")
            if not ("input" in self.samples and "output" in self.samples):
                raise ValidationError("Samples must have 'input' and 'output' keys")
        if self.tests is not None:
            if not isinstance(self.tests, dict):
                raise ValidationError("Tests must be a dictionary.")
            if not ("input" in self.tests and "output" in self.tests):
                raise ValidationError("Samples must have 'input' and 'output' keys")

        return super().save(*args, **kwargs)

    class Meta:
        ordering = ["number"]


class Answer(models.Model):
    """
    Model to store answer sent by participants.
    """

    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    answer_code = models.TextField()
    is_correct_answer = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    time_submitted = models.DateTimeField()
    team_member = models.ForeignKey(
        TeamMember, on_delete=models.CASCADE, related_name="answers"
    )
    team = models.ForeignKey(
        TeamProfile, on_delete=models.CASCADE, related_name="answers"
    )

    test_results = models.JSONField(
        null=True, blank=True
    )  # The key is the test input, the value is the output

    def __str__(self):
        return f"{self.question.number} - {self.team_member.team.team_name} - {self.time_submitted}"


class SharedCode(models.Model):
    """
    Model to store shared code between team members.
    """

    team = models.ForeignKey(
        TeamProfile, on_delete=models.CASCADE, related_name="shared_code"
    )
    code = models.TextField()
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="shared_code"
    )
    time_shared = models.DateTimeField()
    team_member = models.ForeignKey(
        TeamMember, on_delete=models.CASCADE, related_name="shared_code"
    )

    file_uuid = models.UUIDField(default=uuid.uuid4, null=True, blank=True)

    def __str__(self):
        return f"{self.team.team_name} - {self.question.title} - {self.time_shared}"
