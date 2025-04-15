from django.db import models

class Assignment(models.Model):
    title = models.CharField(max_length=105)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    submission_date = models.DateTimeField()

    def __str__(self):
        return self.title
    