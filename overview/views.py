# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets

from overview.models import Customer, Order, Category, Product, Supplier
from overview.serializers import CategorySerializer, CityFilterSerializer, CountryFilterSerializer, CustomerSerializer, OrderSerializer, ProductSerializer, SupplierSerializer

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

# from overview.pagination import PageNumberSizePagination

class OverviewViewSet(APIView):
    
    def get(self, request):

        answer = {'id': "42", 'name': "question"}

        return Response(answer)
    

class OrderViewSet(viewsets.ModelViewSet):
    search_fields = ['product__product_name' , 'customer__country'] # '^' means to search only from start 
    filter_backends = (DjangoFilterBackend, filters.SearchFilter )
    filterset_fields = ['shipped_country', 'shipped_city']#
    queryset = Order.objects.all().order_by('id') #.order_by('id') - to suppress the warning
    serializer_class = OrderSerializer

    # pagination_class = PageNumberSizePagination
    # http_method_names = ['get', 'post', 'patch','delete']
    # return Response(queryset)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# add when adding filtering to backend
class CountryFilterViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.values('shipped_country').distinct()
    serializer_class = CountryFilterSerializer
    paginator = None

class CityFilterViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.values('shipped_city').distinct()
    # queryset = Order.objects.all().distinct()
    serializer_class = CityFilterSerializer
    paginator = None

