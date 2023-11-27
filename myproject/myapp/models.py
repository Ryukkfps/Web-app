from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models

class GeneratedFile(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='generated_files/')

    def __str__(self):
        return self.name


