from django.db import models

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=30)
    desc=models.TextField()
    image=models.ImageField(upload_to="categories")

    def __str__(self):
        return self.name

class Product(models.Model):
    name=models.CharField(max_length=20)
    image=models.ImageField(upload_to="product")
    desc=models.TextField()
    price=models.IntegerField()
    stock=models.IntegerField()
    available=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)  #one time
    updated=models.DateTimeField(auto_now=True)       # Each time we update record

    category=models.ForeignKey(Category,on_delete=models.CASCADE)    # foreign key Reference to category table

