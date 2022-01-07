from django.db import models


# Create your models here.


class Movie(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField()
    duration = models.IntegerField()

    def __str__(self):
        return self.name
