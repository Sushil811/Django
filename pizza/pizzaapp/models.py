from django.db import models

class PizzModel(models.Model):
    name = models.CharField(max_length=10)
    price = models.CharField(max_length=10)

class CustomerModel(models.Model):
    username = models.CharField(max_length=10)
    phoneno = models.CharField(max_length=10)

class OrderModel(models.Model):
    username = models.CharField(max_length=10)
    phoneno = models.CharField(max_length=10)
    address = models.CharField(max_length=10)
    ordereditems = models.CharField(max_length=10)