from django.urls import include, path
from rest_framework.routers import SimpleRouter
from store.views import ProductViewSet


router = SimpleRouter()
router.register("products", ProductViewSet, basename="product")

urlpatterns = [path("", include(router.urls))]
