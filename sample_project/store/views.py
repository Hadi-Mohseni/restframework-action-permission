from restframework_action_permission import ActionPermission
from rest_framework.viewsets import ModelViewSet
from store.serializers import ProductSerializer
from store.models import Product


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [ActionPermission]
    serializer_class = ProductSerializer
