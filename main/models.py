from django.db import models

# Create your models here.

from django.db import models

class FormData(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=128)
    checkbox = models.BooleanField(default=False)

    def __str__(self):
        return self.email
