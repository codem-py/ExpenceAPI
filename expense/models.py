from django.db import models
from django.db.models import Model, CharField, TextChoices, ImageField, TextField, ForeignKey, CASCADE, DecimalField, \
    DateTimeField


class Category(Model):
    class Status(TextChoices):
        INCOME = 'income', 'Income'
        EXPENSES = 'expenses', 'Expenses'
    name  = CharField(max_length=255)
    type = CharField(max_length=100, choices=Status.choices)
    icon = ImageField(upload_to='media/icons/')


class Expense(Model):
    class Status(TextChoices):
        PAYMENTS = 'payments', 'Payments'
        INCOME = 'income', 'Income'

    price = DecimalField(max_digits=9, decimal_places=2)
    type = CharField(max_length=100, choices=Status.choices)
    description = TextField()
    category = ForeignKey('expense.Category', CASCADE, related_name='expenses')
    user = ForeignKey('apps.User', CASCADE, related_name='expenses')
    created_at = DateTimeField(auto_now_add=True)



