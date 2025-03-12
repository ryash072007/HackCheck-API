from django.core.exceptions import ValidationError
from django.db import models

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

