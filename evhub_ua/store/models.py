from django.db import models
from autoslug import AutoSlugField
from django.utils.text import slugify
import os


# функція для генерації імені для зображень товару
def generate_filename(instance, filename):
	base_filename, file_extension = os.path.splitext(filename)
	new_filename = f"{slugify(base_filename)}_{instance.pk}{file_extension}"
	return os.path.join('images/', new_filename)

class Gallery(models.Model):
	title = models.CharField("Ім\'я файлу", max_length=200, blank=True)
	images = models.ImageField('Галерея фото', upload_to=generate_filename)

	class Meta:
		verbose_name = 'Галерея фото'
		verbose_name_plural = 'Галерея фото'

	def __str__(self):
		return self.images.url

	def save(self, *args, **kwargs):
		# Вказуємо автоматичне стоврення імені файлу якщо title порожній
		if not self.title:
			self.title = os.path.basename(self.images.name)

		super().save(*args, **kwargs)

class Category(models.Model):
	title = models.CharField(max_length=55)
	slug = models.SlugField(max_length=50)

	class Meta:
		verbose_name_plural = 'Категорії'

	def __str__(self):
		return self.title

class ChargerItemModel(models.Model):
	title = models.CharField(max_length=50)
	category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)
	description = models.TextField('Короткий опис', max_length=200, null=True)
	image = models.ImageField()
	slug = models.SlugField(max_length=50)

	class Meta:
		verbose_name_plural = 'Модель товару'

	def __str__(self):
		return self.title

class ChargersItems(models.Model):
	TYPE_CHOICES = [
		('Type 1', 'type_1'), ('Type 2', 'type_2'), ('Type Tesla', 'type_tesla')
	]
	PHASES_CHOICES = [
		('Одна фаза', '1_phase'), ('Три фази', '3_phase')
	]
	IN_STOCK_CHOICES = [
		('True', 'Активно'),
		('False', 'Неактивно'),
		('pending', 'Під замовлення'),
	]

	title = models.CharField('Назва', max_length=70)
	slug = AutoSlugField(populate_from='title', max_length=40, unique=True, default=None)
	price = models.DecimalField('Ціна', max_digits=8, decimal_places=2)
	small_description = models.TextField('Короткий опис', max_length=600)
	description = models.TextField('Опис')
	power = models.DecimalField('Потужність, кВт', max_digits=8, decimal_places=1)
	power_amps = models.IntegerField('Потужність, А')
	phases = models.TextField('Кількість фаз', null=True, choices=PHASES_CHOICES)
	type = models.CharField('Тип роз\'єму', max_length=10, null=True, blank=True, choices=TYPE_CHOICES)
	cable_length = models.IntegerField('Довжина кабелю')
	protection = models.CharField('Захист корпусу', max_length=10, null=True, blank=True)
	guarantee = models.CharField('Гарантія', max_length=10)
	brand = models.CharField('Бренд', max_length=20)
	country = models.CharField('Країна-виробник', max_length=20)
	form = models.CharField('Формфактор', max_length=15, null=True, blank=True)
	features = models.TextField('Додаткові функції', max_length=200, null=True, blank=True)
	time = models.DateTimeField('Дата створення', auto_now_add=True, null=True)
	model = models.ForeignKey(ChargerItemModel, null=True, blank=True, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)
	in_stock = models.CharField('Наявність', null=True, blank=True, choices=IN_STOCK_CHOICES)

	class Meta:
		verbose_name_plural = 'Зарядні пристрої'

	def __str__(self):
		return self.title


# додаткові зображення товару
class AttachmentChargersItems(models.Model):
	chargeritem = models.ForeignKey(ChargersItems, on_delete=models.CASCADE, null=True)
	gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, null=True)


# Класи для аксесуарів

class Accessories(models.Model):
	IN_STOCK_CHOICES = [
		('True', 'Активно'),
		('False', 'Неактивно'),
		('pending', 'Під замовлення'),
	]

	title = models.CharField("Ім\'я файлу", max_length=200)
	slug = AutoSlugField(populate_from='title', max_length=40, unique=True, default=None)
	small_description = models.TextField('Короткий опис', null=True, max_length=600)
	description = models.TextField('Опис', null=True)
	size = models.CharField("Розмір", max_length=15)
	material = models.CharField("Матеріал", max_length=50)
	brand = models.CharField("Бренд", max_length=50)
	price = models.IntegerField('Ціна', null=True)
	country = models.CharField('Країна-виробник', null=True, max_length=20)
	in_stock = models.CharField('Наявність', null=True, blank=True, choices=IN_STOCK_CHOICES)
	chargeritem = models.ForeignKey(ChargerItemModel, null=True, blank=True, on_delete=models.CASCADE, related_name='chargeritem')
	category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)

	class Meta:
		verbose_name = 'Аксесуари'
		verbose_name_plural = 'Аксесуари'

class AttachmentAccessories(models.Model):
	accessory = models.ForeignKey(Accessories, on_delete=models.CASCADE, null=True)
	gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, null=True)
