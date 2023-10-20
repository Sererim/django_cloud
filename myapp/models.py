from datetime import  datetime
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
from PIL import Image

# Create your models here.


class Client(models.Model):
    firstname = models.CharField(max_length=45)
    surname = models.CharField(max_length=45)
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(unique=True)
    date_of_registration = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=50)
    
    def __str__(self):
        return f"Client: {self.firstname} {self.surname}\n" \
               f"Email: {self.email}\nPhone number: {self.phone_number}\n" \
               f"Date of registration is: {self.date_of_registration}\n" \
               f"Address: {self.address}"


class Product(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=256, default=' ')
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0.99)
    amount = models.IntegerField(default=1)
    date_of_addition = models.DateTimeField(auto_now_add=True)
    
    # Additional column in a database that will store images, allows to have no image for a product.
    image = models.ImageField(upload_to='products_images/', blank=True, null=True)
    
    def clean(self) -> None:
        if self.price <= 0:
            raise ValidationError("Price can not be zero or negative.")
        if self.amount <= 0:
            raise ValidationError("Amount can not be zero or negative.")
    
    # Function that will save images.
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            img.save(self.image.path)
    
    
    def __str__(self) -> str:
        return f"Product name: {self.name}\n" \
               f"Desription: {self.description}\n" \
               f"Price: {self.price}. Amount: {self.amount}\n" \
               f"Date of addition to the database: {self.date_of_addition}"


class Order(models.Model):
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    cost = models.DecimalField(decimal_places=2, max_digits=10, default=1)
    date_of_order = models.DateTimeField(auto_now_add=True)
    
    def clean(self) -> None:
        if self.cost <= 0:
            raise ValidationError("Cost can not be zero or negative.")
    
    def __str__(self) -> str:
        return f"Clien ID: {self.client_id}\n" \
               f"Product ID: {self.product_id}" \
               f"Cost: {self.cost}. Date of order: {self.date_of_order}"

