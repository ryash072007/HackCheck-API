from django.core.exceptions import ValidationError
from django.db import models
from db.models.user import TeamMember

class Question(models.Model):
    """
    Model to store questions for the quiz.
    """
    
    title = models.CharField(max_length=300)
    number = models.IntegerField()
    description = models.TextField()

    samples = models.JSONField(null=True, blank=True) # The key is the sample input, the value is the ouput
    
    def __str__(self):
        return self.title
    
    def save(self, force_insert = ..., force_update = ..., using = ..., update_fields = ...):
        samples = self.samples
        if samples is not None:
            if not isinstance(samples, dict):
                raise ValidationError("Samples must be a dictionary.")
            
        return super().save(force_insert, force_update, using, update_fields)

    class Meta:
        ordering = ['number']

class Answer(models.Model):
    """
    Model to store answer sent by participants.
    """
    
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer_code = models.TextField()
    is_correct_answer = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    time_submitted = models.TimeField(auto_now_add=True)
    team = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name='answers')
    
    def __str__(self):
        return self.answer_code