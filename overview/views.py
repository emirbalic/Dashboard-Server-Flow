# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets

from overview.models import Customer, Order, Category, Product, Supplier
from overview.serializers import CategorySerializer, CustomerSerializer, OrderSerializer, ProductSerializer, SupplierSerializer


class OverviewViewSet(APIView):
    
    def get(self, request):

        answer = {'id': "42", 'name': "question"}

        return Response(answer)
    

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
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

