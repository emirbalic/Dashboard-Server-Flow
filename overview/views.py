# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets

from overview.models import Customer, Order, Category, Product, Supplier
from overview.serializers import CategorySerializer, CustomerSerializer, OrderSerializer, ProductSerializer, SupplierSerializer

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class OverviewViewSet(APIView):
    
    def get(self, request):

        answer = {'id': "42", 'name': "question"}

        return Response(answer)
    

class OrderViewSet(viewsets.ModelViewSet):
    search_fields = ['shipped_name', 'customer__last_name'] # '^' means to search only from start
    filter_backends = (DjangoFilterBackend, filters.SearchFilter )
    filterset_fields = ['shipped_country', 'shipped_city']#
    queryset = Order.objects.all().order_by('id') #.order_by('id') - to suppress the warning
    serializer_class = OrderSerializer


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

