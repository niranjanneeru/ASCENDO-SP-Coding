from django.db import models


class Rules(models.Model):
    priority = models.PositiveSmallIntegerField(unique=True)
    rule = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.priority)

    class Meta:
        verbose_name_plural = 'Rules'
        verbose_name = 'Rule'
