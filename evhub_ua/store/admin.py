from django.contrib import admin
from .models import ChargerItemModel, Category, ChargersItems, Attachment
from django.utils.html import format_html

class AttachmentInline(admin.TabularInline):
    model = Attachment

class ChargersItemsAdmin(admin.ModelAdmin):
    inlines = [
        AttachmentInline,
]

admin.site.register(Category)
admin.site.register(ChargerItemModel)
admin.site.register(ChargersItems, ChargersItemsAdmin)
admin.site.register(Attachment)

