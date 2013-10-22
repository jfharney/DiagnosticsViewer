from django.db import models

class Diags(models.Model):
  state = models.CharField(max_length=200)


# Create your models here.
