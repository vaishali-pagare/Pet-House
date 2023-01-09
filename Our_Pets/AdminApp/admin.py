from django.contrib import admin
from .models import Category,Pets,Pet_Cat,PaymentMaster

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display= ("id","category_name")

class PetsAdmin(admin.ModelAdmin):
    list_display = ("id","pname","image","cat")

class Pet_Cat_Admin(admin.ModelAdmin):
    list_display = ("id","pet","category","image","price","front","side","description","lifespan","weight","height")
    
class PaymentMasterAdmin(admin.ModelAdmin):
    list_display= ("id","cardno","cvv","expiry","balance","mobile")

admin.site.register(Category, CategoryAdmin)
admin.site.register(Pets,PetsAdmin)
admin.site.register(Pet_Cat,Pet_Cat_Admin)
admin.site.register(PaymentMaster,PaymentMasterAdmin)