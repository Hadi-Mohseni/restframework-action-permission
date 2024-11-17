from django.contrib.auth.models import User, Permission
from store.views import ProductViewSet
from store.models import Product
from django.urls import resolve, reverse
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate


class TestRetrieveAction(APITestCase):
    fixtures = ["product.json", "user.json"]

    def setUp(self) -> None:
        product = Product.objects.first()
        self.url = reverse("product-detail", kwargs={"pk": product.id})
        self.view = ProductViewSet.as_view({"delete": "destroy"})
        return super().setUp()

    def test_if_url_correctly_resolved(self):
        """
        Test if url will be correctly resolved to product-retrieve view.
        """
        product = Product.objects.first()
        view = resolve(f"/products/{product.id}/")
        self.assertEqual(view.view_name, "product-detail")

    def test_if_user_without_permission_can_not_delete(self):
        """
        Test if an user without delete_product permission can not delete.
        """
        user = User.objects.first()
        product = Product.objects.first()
        factory = APIRequestFactory()
        request = factory.delete(self.url)
        force_authenticate(request, user)
        response = self.view(request, pk=product.id)
        self.assertEqual(response.status_code, 403)

    def test_if_user_with_permission_can_delete(self):
        """
        Test if an user with delete_view permission can delete.
        """
        product = Product.objects.first()
        user = User.objects.first()
        permission = Permission.objects.get(codename="delete_product")
        user.user_permissions.add(permission)
        factory = APIRequestFactory()
        request = factory.delete(self.url)
        force_authenticate(request, user)
        response = self.view(request, pk=product.id)
        self.assertEqual(response.status_code, 204)
