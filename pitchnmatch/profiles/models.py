from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length = 100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pitch = models.TextField()

    def __str__(self):
        return f"projet de {self.user.username}"


class MatchResult(models.Model):
    project1 = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='matches_as_p1')
    project2 = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='matches_as_p2')
    score = models.IntegerField(default=0)
    explanation = models.TextField()

    class Meta:
        unique_together = ('project1', 'project2')

    def __str__(self):
        return f"Match {self.project1.name} - {self.project2.name} : {self.score}%"
