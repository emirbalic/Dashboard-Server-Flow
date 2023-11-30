# from django.urls import path

# from overview.views import OverviewViewSet


from django.urls import include, path

from overview.views import CategoryViewSet, CustomerViewSet, OrderViewSet, OverviewViewSet, ProductViewSet, SupplierViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('orders', OrderViewSet, basename='orders')
router.register('categories', CategoryViewSet, basename='categories')
router.register('customers', CustomerViewSet, basename='customers')
router.register('suppliers', SupplierViewSet, basename='suppliers')
router.register('products', ProductViewSet, basename='products')

urlpatterns = [
    path('overview/', OverviewViewSet.as_view(), name='overview'),
    path('', include(router.urls)),
]