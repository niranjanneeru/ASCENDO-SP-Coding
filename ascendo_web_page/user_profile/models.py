from django.conf import settings
from django.db import models
from django.db.models import Q

class Profile(models.Model):
    name = models.CharField(max_length=100)
    nick_name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    college = models.CharField(max_length=100)
    language = models.BooleanField(default=False)
    code = models.BooleanField(default=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    has_completed = models.BooleanField(default=False)
    last_submission = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Profile"
        ordering = ('-has_completed', 'last_submission', '-code', '-has_completed')
