from django.db import models


# Create your models here.
class Members(models.Model):
    nickname = models.CharField(max_length=200)
    kakaotalk_cord = models.CharField(primary_key=True, max_length=200)
