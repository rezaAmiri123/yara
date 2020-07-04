from django.contrib import admin
from products.models import Brand, Product


class BrandAdmin(admin.ModelAdmin):
    list_display = ('email', 'company_name')
    raw_id_fields = ('city', 'time_zone')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Brand, BrandAdmin)
admin.site.register(Product, ProductAdmin)
