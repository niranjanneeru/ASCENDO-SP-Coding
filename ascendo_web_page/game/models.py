from django.db import models

from ascendo_web_page.user_profile.models import Profile


class Question(models.Model):
    question = models.CharField(max_length=500)
    answer = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    image = models.URLField(max_length=500)

    def __str__(self):
        return self.question


class Challenge(models.Model):
    question = models.CharField(max_length=500)
    is_active = models.BooleanField(default=False)
    image = models.URLField(max_length=500)
    answer = models.TextField()

    def __str__(self):
        return self.question


class Response(models.Model):
    CHOICES = ((1, "Correct Answer"), (0, "Wrong Answer"))
    answer = models.TextField()
    create_date = models.DateTimeField()
    status = models.PositiveSmallIntegerField(choices=CHOICES, default=0)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
