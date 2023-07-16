from django.urls import path
from core.services import product, user, cart, order, product_category, product_inventory

from core.views import ProfileView, RegistrationView


app_name = 'core'

urlpatterns = [
    path('', product.ProductService.get_all_products, name='home'),
    
    path('sign-up/', RegistrationView.as_view(), name='sign_up'),
    path('profile/', ProfileView.as_view(), name='profile'),
    
    path('get-user/<int:id>', user.UserService.get_user),
    path('update-user/<int:id>', user.UserService.update_user),
    path('delete-user/<int:id>', user.UserService.delete_user),
    path('get-all-users', user.UserService.get_all_user),
    
    path('create-new-product', product.ProductService.create_product),
    path('get-product/<int:id>', product.ProductService.get_product),
    path('update-product/<int:id>', product.ProductService.update_product),
    path('delete-product/<int:id>', product.ProductService.delete_product),
    path('get-all-products', product.ProductService.get_all_products),
    
    path('create-product-category', product_category.ProductCategoryService.create_product_category),
    path('get-product-category/<int:id>', product_category.ProductCategoryService.get_product_category),
    path('update-product-category/<int:id>', product_category.ProductCategoryService.update_product_category),
    path('delete-product-category/<int:id>', product_category.ProductCategoryService.delete_product_category),
    path('get-all-product-categories', product_category.ProductCategoryService.get_all_product_categories),
    path('add-product-to-category/<int:id>', product_category.ProductCategoryService.add_product_to_category),
    path('remove-product-from-category', product_category.ProductCategoryService.remove_product_from_category),
    
    path('create-product-category-inventory', product_inventory.ProductInventoryService.create_product_category_inventory),
    path('get-product-category-inventory/<int:id>', product_inventory.ProductInventoryService.get_product_category_inventory_by_id),
    path('update-product-category-inventory/<int:id>', product_inventory.ProductInventoryService.update_product_category_inventory),
    path('delete-product-category-inventory/<int:id>', product_inventory.ProductInventoryService.delete_product_category_inventory),
    path('get-all-product-category-inventory', product_inventory.ProductInventoryService.get_all_product_category_inventory),
    path('get-product-category-inventory-by-product', product_inventory.ProductInventoryService.get_product_category_inventory_by_product),
    
    path('create-order', order.OrderService.create_order),
    path('get-order/<int:id>', order.OrderService.get_order),
    path('update-order/<int:id>', order.OrderService.update_order),
    path('delete-order/<int:id>', order.OrderService.delete_order),
    
    path('create-cart', cart.CartService.create_cart),
    path('get-cart/<int:id>', cart.CartService.get_cart),
    path('update-cart/<int:id>', cart.CartService.update_cart),
    path('delete-cart/<int:id>', cart.CartService.delete_cart),
    path('clear-cart', cart.CartService.clear_cart),
    
    ##########################   Functional requirement APIS   ##########################
    path('get-all-products-cart', cart.CartService.get_all_products_in_cart),
    path('add-product-to-cart', cart.CartService.add_product_to_cart),
    path('remove-product-from-cart', cart.CartService.remove_product_from_cart),
    path('update-product-count-in-cart', cart.CartService.update_product_count_in_cart),
    path('checkout-with-order', cart.CartService.checkout_and_place_order),
    path('get-all-orders', order.OrderService.get_all_orders),
    path('get-all-orders-by-user', order.OrderService.get_all_orders_by_user),
 
    
    ]