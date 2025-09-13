from django.db import models
class Category(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=250)
    desc = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True,default='product_images/default.jpg')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)


    def __str__(self):
        return self.name
