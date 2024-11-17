from django.contrib.auth.models import User, Permission
from store.views import ProductViewSet
from django.urls import resolve, reverse
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate


class TestListAction(APITestCase):
    fixtures = ["product.json", "user.json"]

    def setUp(self) -> None:
        self.url = reverse("product-list")
        self.view = ProductViewSet.as_view({"post": "create"})
        return super().setUp()

    def test_if_url_correctly_resolved(self):
        """
        Test if url will be correctly resolved to product-list view.
        """
        view = resolve("/products/")
        self.assertEqual(view.view_name, "product-list")

    def test_if_user_without_permission_can_not_create(self):
        """
        Test if an user without add_product permission can not create new products.
        """
        user = User.objects.first()
        factory = APIRequestFactory()
        request = factory.post(self.url, data={"name": "product_two"})
        force_authenticate(request, user)
        response = self.view(request)
        self.assertEqual(response.status_code, 403)

    def test_if_user_with_permission_can_create(self):
        """
        Test if an user with add_product permission can create new products.
        """
        user = User.objects.first()
        permission = Permission.objects.get(codename="add_product")
        user.user_permissions.add(permission)
        factory = APIRequestFactory()
        request = factory.post(self.url, data={"description": "product_two"})
        force_authenticate(request, user)
        response = self.view(request)
        self.assertEqual(response.status_code, 201)
