from django.db import models
from wp_1 import *

# Create your models here.


class details(models.Model):
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=500)
    date = models.CharField(max_length=500)
    website = models.CharField(max_length=500)
    duration = models.CharField(max_length=500)
    link = models.CharField(max_length=500)
