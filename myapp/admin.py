from django.contrib import admin
from .models import Client, Product, Order

# Register your models here.

@admin.action(description="Product is out of stock.")
def out_of_stock(modeladmin, request, queryset) -> None:
    queryset.update(amount=0)


class ClientAdmin(admin.ModelAdmin):
    list_display = ['id', 'firstname', 'surname', 'email',
                    'phone_number', 'address', 'date_of_registration']
    ordering = ['id', '-surname']
    list_filter = ['date_of_registration', 'address']
    search_fields = ['surname', 'address', 'phone_number']
    readonly_fields = ['date_of_registration']
    
    fieldsets = [
        (
            'Client',
            {
                'classes': ['collapse'],
                'description': "Client's legal info.",
                'fields': ['firstname', 'surname',
                           'phone_number', 'address'], 
            }    
        ),
        (
            'Site info',
            {
                'description': "Client's site info",
                'fields': ['email', 'date_of_registration'],
            }    
        )
    ]


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description',
                    'price', 'amount']
    ordering = ['id', '-price', '-amount']
    list_filter = ['price', 'amount']
    search_fields = ['name', 'price']
    actions = [out_of_stock]
    
    fields = ['name', 'price', 'date_of_addition', 'amount', 'description']
    readonly_fields = ['date_of_addition']
    

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'client_id', 'product_id',
                    'cost', 'date_of_order']
    ordering = ['id']
    list_filter = ['product_id', 'client_id', 'date_of_order']
    search_fields = ['client_id', 'product_id']
    
    fields = ['client_id', 'product_id', 'date_of_order']
    readonly_fields = ['date_of_order']
    

admin.site.register(Client, ClientAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
