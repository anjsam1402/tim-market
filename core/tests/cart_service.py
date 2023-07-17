# from django.contrib.auth import get_user_model
# from django.test import TestCase, TransactionTestCase
# from django.urls import reverse
# import core
# from core.forms import RegistrationForm

# from core.models import Product, User
# from core.services.product import ProductService


# class CartServiceTests(mTestCase):

#    def setUp(self):

#       product_data = {
#          "name": "test_product",
#          "category_price_list": [
#             {
#                   "category_id": 4,
#                   "price": 105.955,
#                   "quantity": 150
#             }
#          ]
#       }
#       self.product = Product.objects.create(name=product_data["name"])
#       self.product_category_response_list = ProductService._create_product_category_details(self.product.id, product_data)

#    def test_add_product_to_cart(self):
#       data = {
#          "username": "testuser3",
#          "name": "testuser",
#          "email": "testuser@gmail.com",
#          "password": "password123",
#          "is_superuser": True
#       }
#       User = get_user_model()
#       self.user = User.objects.create_superuser(**data)
#       self.body = {
#          "product_id": self.product.id,
#          "category_id": 4,
#          "quantity": 9
#       }
#       print("reverse('add-product-to-cart')")
#       print(self)
#       print(reverse('core:add-product-to-cart'))
#       self.assertEqual(self.user.email, "testuser@gmail.com")
#       self.client.force_login(self.user)
#       response = self.client.post(reverse('core:add-product-to-cart'), self.body, content_type="application/json")
#       print(response)


#    def test_get_all_products_in_cart(self):
#       pass
