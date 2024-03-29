from django.contrib import admin
from .models import ChargerItemModel, Category, ChargersItems, AttachmentChargersItems,\
    Accessories, AttachmentAccessories, Gallery
from django.utils.html import format_html


admin.site.register(Category)
admin.site.register(ChargerItemModel)


class GalleryAdmin(admin.ModelAdmin):

    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:150px; max-height:150px"/>'.format(obj.images.url))

    list_display = ['title', 'image_tag']


admin.site.register(Gallery, GalleryAdmin)


class AttachmentChargersItemsInline(admin.TabularInline):
    model = AttachmentChargersItems
    extra = 1  # Додаткові поля для видалення
    can_delete = True



class ChargersItemsAdmin(admin.ModelAdmin):
    inlines = [
        AttachmentChargersItemsInline,
    ]


admin.site.register(ChargersItems, ChargersItemsAdmin)


class AttachmentAccessoriesInline(admin.TabularInline):
    model = AttachmentAccessories
    extra = 1


class AccessoriesAdmin(admin.ModelAdmin):
    inlines = [AttachmentAccessoriesInline]


admin.site.register(Accessories, AccessoriesAdmin)

