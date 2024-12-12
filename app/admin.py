from django.contrib import admin
from .models import *
# from .models import (
#     FilterYear,
#     Images,
#     Tag,  # Corrected import
#     VehicleMake,
#     VehicleModel,
#     Category,
#     Product,
#     Order,
#     OrderItem,
#     Address,
#     Review,
#     ProductRating
# )

# class VehicleMakeAdmin(admin.ModelAdmin):
#     list_display = ('name', 'description')
#     search_fields = ('name', 'description')

# class VehicleModelAdmin(admin.ModelAdmin):
#     list_display = ('make', 'name', 'description')
#     search_fields = ('make__name', 'name', 'description')

# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('name', 'description')
#     search_fields = ('name', 'description')

# class FilterYearAdmin(admin.ModelAdmin):  # Added admin class for FilterYear
#     list_display = ('year',)
#     search_fields = ('year',)

# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('name', 'price', 'category', 'vehicle_make', 'vehicle_model')
#     search_fields = ('name', 'description', 'category__name', 'vehicle_make__name', 'vehicle_model__name')

# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('user', 'total', 'status')
#     search_fields = ('user__username', 'total', 'status')

# class OrderItemAdmin(admin.ModelAdmin):
#     list_display = ('order', 'product', 'quantity')
#     search_fields = ('order__user__username', 'product__name', 'quantity')

# class AddressAdmin(admin.ModelAdmin):
#     list_display = ('user', 'street', 'city', 'state', 'zip_code', 'country')
#     search_fields = ('user__username', 'street', 'city', 'state', 'zip_code', 'country')

# class ReviewAdmin(admin.ModelAdmin):
#     list_display = ('user', 'product', 'rating', 'feedback')
#     search_fields = ('user__username', 'product__name', 'rating', 'feedback')

# class ProductRatingAdmin(admin.ModelAdmin):
#     list_display = ('product', 'average_rating', 'total_reviews')
#     search_fields = ('product__name', 'average_rating', 'total_reviews')


class ImagesTublerinline(admin.TabularInline):
    model=Images


class TagTublerinline(admin.TabularInline):
    model=Tag

class ProductAdmin(admin.ModelAdmin):
    inlines = [ImagesTublerinline,TagTublerinline]

class OrderItemTublerinline(admin.TabularInline):
    model=OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemTublerinline]

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(FilterYear)  # Updated to use its a price
admin.site.register(Product,ProductAdmin)
admin.site.register(Images)
admin.site.register(Tag)
admin.site.register(Contact_us)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem)

