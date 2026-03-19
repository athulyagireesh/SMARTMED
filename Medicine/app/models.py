from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    image = models.ImageField(upload_to='products/')
    category = models.CharField(max_length=100)
    description = models.TextField()

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

def __str__(self):
    return f"{self.user.username} - {self.product.name}"

    def __str__(self):
        return self.name