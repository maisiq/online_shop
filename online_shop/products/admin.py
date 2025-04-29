from django.contrib import admin

from .models import Category, Discount, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'hierarchy', 'slug']
    list_select_related = ['parent']

    prepopulated_fields = {
        'slug': ['name'],
    }

    def hierarchy(self, obj):
        return ' -> '.join(anc.name for anc in obj.get_ancestors(include_self=True))


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'hierarchy']
    list_select_related = ['category']

    def hierarchy(self, obj):
        return ' -> '.join(anc.name for anc in obj.category.get_ancestors(include_self=True))


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['type', 'name', 'value', 'start_at', 'expired_at', 'is_active']