from django.db import models


class Item(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()  # Добавлено поле для количества товара
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Добавлено поле для общей стоимости товара

    def __str__(self):
        return self.title
