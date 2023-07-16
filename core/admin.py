from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.forms import UserChangeForm, UserCreationForm

from core.models import (
   User, Cart, Product, OrderTable, 
   CartProductMap, CartUserMap, 
   CartPriceMap, UserOrderMap, OrderProductMap, 
   OrderStatus, ProductCategoryPriceMap, 
   ProductCategoryMap, ProductInventoryMap
)

class CoreUserAdmin(UserAdmin):
   
   form = UserChangeForm
   add_form = UserCreationForm

   list_display = ('username', 'email', 'name', 'is_staff',  'is_superuser')
   list_filter = ('is_superuser',)

   fieldsets = (
      (None, {'fields': ('username', 'name', 'email', 'is_staff', 'is_superuser', 'password')}),
      # ('Personal info', {'fields': ('name',)}),
      # ('Groups', {'fields': ('groups',)}),
      # ('Permissions', {'fields': ('user_permissions',)}),
   )
   add_fieldsets = (
      (None, {'fields': ('username', 'name', 'email', 'is_staff', 'is_superuser', 'password1', 'password2')}),
      # ('Personal info', {'fields': ('name')}),
      # ('Groups', {'fields': ('groups',)}),
      # ('Permissions', {'fields': ('user_permissions',)}),
   )

   search_fields = ('email', 'name', 'username')
   ordering = ('username',)
   filter_horizontal = ()


admin.site.register(User, CoreUserAdmin)
admin.site.register(UserOrderMap)

admin.site.register(Product)
admin.site.register(ProductCategoryMap)
admin.site.register(ProductCategoryPriceMap)
admin.site.register(ProductInventoryMap)


admin.site.register(Cart)
admin.site.register(CartProductMap)
admin.site.register(CartUserMap)
admin.site.register(CartPriceMap)


admin.site.register(OrderTable)
admin.site.register(OrderStatus)
admin.site.register(OrderProductMap)

