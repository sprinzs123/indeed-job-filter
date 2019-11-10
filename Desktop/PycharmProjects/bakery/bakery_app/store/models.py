from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=220)
    price = models.IntegerField(max_length=12)
    picture = models.ImageField(upload_to='images/')
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.title