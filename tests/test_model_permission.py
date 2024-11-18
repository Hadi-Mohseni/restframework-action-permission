from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from django.contrib.auth.models import User, Permission
from django.urls import resolve, reverse
from store.views import ProductViewSet
from store.models import Product


class TestCreateAction(APITestCase):
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


class TestDeleteAction(APITestCase):
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


class TestListAction(APITestCase):
    fixtures = ["product.json", "user.json"]

    def setUp(self) -> None:
        self.url = reverse("product-list")
        self.view = ProductViewSet.as_view({"get": "list"})
        return super().setUp()

    def test_if_url_correctly_resolved(self):
        """
        Test if url will be correctly resolved to product-list view.
        """
        view = resolve("/products/")
        self.assertEqual(view.view_name, "product-list")

    def test_if_user_without_permission_can_not_get_all_products(self):
        """
        Test if an user without product_list permission can not get all products.
        """
        user = User.objects.first()
        factory = APIRequestFactory()
        request = factory.get(self.url)
        force_authenticate(request, user)
        response = self.view(request)
        self.assertEqual(response.status_code, 403)

    def test_if_user_with_permission_can_get_all_products(self):
        """
        Test if an user with direct product_list permission can get all products.
        """
        user = User.objects.first()
        permission = Permission.objects.get(codename="list_product")
        user.user_permissions.add(permission)
        factory = APIRequestFactory()
        request = factory.get(self.url)
        force_authenticate(request, user)
        response = self.view(request)
        self.assertEqual(response.status_code, 200)


class TestRetrieveAction(APITestCase):
    fixtures = ["product.json", "user.json"]

    def setUp(self) -> None:
        product = Product.objects.first()
        self.url = reverse("product-detail", kwargs={"pk": product.id})
        self.view = ProductViewSet.as_view({"get": "retrieve"})
        return super().setUp()

    def test_if_url_correctly_resolved(self):
        """
        Test if url will be correctly resolved to product-retrieve view.
        """
        product = Product.objects.first()
        view = resolve(f"/products/{product.id}/")
        self.assertEqual(view.view_name, "product-detail")

    def test_if_user_without_permission_can_not_get_products_detail(self):
        """
        Test if an user without product_view permission can not get products_detail.
        """
        user = User.objects.first()
        product = Product.objects.first()
        factory = APIRequestFactory()
        request = factory.get(self.url)
        force_authenticate(request, user)
        response = self.view(request, pk=product.id)
        self.assertEqual(response.status_code, 403)

    def test_if_user_with_permission_get_products_detail(self):
        """
        Test if an user with product_view permission can get products detail.
        """
        product = Product.objects.first()
        user = User.objects.first()
        permission = Permission.objects.get(codename="view_product")
        user.user_permissions.add(permission)
        factory = APIRequestFactory()
        request = factory.get(self.url)
        force_authenticate(request, user)
        response = self.view(request, pk=product.id)
        self.assertEqual(response.status_code, 200)


class TestUpdateAction(APITestCase):
    fixtures = ["product.json", "user.json"]

    def setUp(self) -> None:
        product = Product.objects.first()
        self.url = reverse("product-detail", kwargs={"pk": product.id})
        self.view = ProductViewSet.as_view({"put": "update"})
        return super().setUp()

    def test_if_url_correctly_resolved(self):
        """
        Test if url will be correctly resolved to product-retrieve view.
        """
        product = Product.objects.first()
        view = resolve(f"/products/{product.id}/")
        self.assertEqual(view.view_name, "product-detail")

    def test_if_user_without_permission_can_not_update(self):
        """
        Test if an user without change_product permission can not update.
        """
        user = User.objects.first()
        product = Product.objects.first()
        factory = APIRequestFactory()
        request = factory.put(self.url)
        force_authenticate(request, user)
        response = self.view(request, pk=product.id)
        self.assertEqual(response.status_code, 403)

    def test_if_user_with_permission_can_update(self):
        """
        Test if an user with change_product permission can update.
        """
        product = Product.objects.first()
        user = User.objects.first()
        permission = Permission.objects.get(codename="change_product")
        user.user_permissions.add(permission)
        factory = APIRequestFactory()
        request = factory.put(self.url, data={"description": "product_1"})
        force_authenticate(request, user)
        response = self.view(request, pk=product.id)
        self.assertEqual(response.status_code, 200)
