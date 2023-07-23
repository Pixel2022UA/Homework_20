import os

import requests
from dotenv import load_dotenv
from django.db import models

load_dotenv()
mono_token = os.getenv("MONOBANK_API_KEY")


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.CharField(max_length=100)
    publication_date = models.DateField()
    quantity = models.IntegerField()
    price = models.PositiveIntegerField()


class Order(models.Model):
    books = models.ManyToManyField(Book, through="OrderItems")
    total_price = models.IntegerField()
    create = models.DateTimeField(auto_now_add=True)
    invoice_id = models.CharField(max_length=500, null=True)
    status = models.CharField(max_length=200, null=True)


class OrderItems(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class MonoSettings(models.Model):
    public_key = models.CharField(max_length=1000)

    @classmethod
    def get_token(cls):
        try:
            return cls.objects.last().public_key
        except AttributeError:
            key = requests.get(
                "https://api.monobank.ua/api/merchant/pubkey",
                headers={"X-Token": mono_token},
            ).json()["key"]
            cls.objects.create(public_key=key)
            return key
