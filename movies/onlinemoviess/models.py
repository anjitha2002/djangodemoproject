from django.db import models
class Movie(models.Model):
    title=models.CharField(max_length=20)
    description=models.TextField(max_length=200)
    language=models.CharField(max_length=20)
    year=models.IntegerField()
    image=models.ImageField(upload_to='images')
# Create your models here.
