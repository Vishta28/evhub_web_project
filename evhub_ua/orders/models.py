from django.db import models

from store.models import ChargersItems


class Order(models.Model):
	ORDER_STATUS = [
		('ordered', 'Нове замовлення'), ('shipped', 'Доставлено'), ('refusal', 'Відмова')
	]
	# SHIPPING_TYPE = [
	# 	('nova_poshta', 'Нова Пошта'), ('self', 'Самовивіз'), ('refusal', 'Відмова')
	# ]

	user = models.CharField(max_length=50)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50, null=True, blank=True)
	phone_number = models.CharField(max_length=15)
	total_cost = models.IntegerField(default=0)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=20, choices=ORDER_STATUS, default='ordered')

	class Meta:
		ordering = ('-created',)
		verbose_name = 'Замовлення'
		verbose_name_plural = 'Замовлення'


class OrderItem(models.Model):
	order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
	product = models.ForeignKey(ChargersItems, related_name='order_items', on_delete=models.CASCADE)
	price = models.IntegerField()
	quantity = models.IntegerField(default=1)
