from django.contrib import admin
from .models import ChargerItemModel, Category, ChargersItems

admin.site.register(Category)
admin.site.register(ChargerItemModel)
admin.site.register(ChargersItems)

