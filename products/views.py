from xml.etree.ElementPath import prepare_parent

from django.shortcuts import render
from django.core.serializers import serialize
from django.template.defaulttags import comment
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from django.db.models import Q
from .models import Product
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import render

# Create your views here.

class ProductListApi(APIView):
    def get(self, request):
        products = Product.objects.all()

        category = request.GET.get('category')
        if category:
            products = products.filter(category__name=category)

        search = request.GET.get('search')
        if search:
            products = products.filter(
                Q(name__icontains=search)
            )
        price_gt = request.GET.get('price_gt')
        if price_gt:
            products = products.filter(price__gt=price_gt)

        price_lt = request.GET.get('price_lt')
        if price_lt:
            products = products.filter(price__lt=price_lt)

        ordering = request.GET.get('ordering')
        if ordering:
            products = products.order_by(ordering)

        paginator = LimitOffsetPagination()
        paginator.page_size = 4
        paginated_product = paginator.paginate_queryset(products, request)

        serializer = ProductSerializer(paginated_product, many=True)
        data = {
            'data': serializer.data,
            'count': len(products),
            'status': status.HTTP_200_OK
        }
        return paginator.get_paginated_response(data)

    def post(self, request):
        if not request.user.is_staff:
            return Response({'errors':'Sizga ruxsat yoq', 'status':status.HTTP_403_FORBIDDEN})

        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductUpdateDetailDeleteApi(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return None

    def get(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response({'err':'Mahsulot topilmadi', 'status':status.HTTP_400_BAD_REQUEST})
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        if not request.user.is_staff:
            return Response({'error': 'Sizda ruxsat yo‘q!'}, status=status.HTTP_403_FORBIDDEN)

        product = self.get_object(pk)
        if not product:
            return Response({'error': 'Mahsulot topilmadi'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if not request.user.is_staff:
            return Response({'error': 'Sizda ruxsat yo‘q!'}, status=status.HTTP_403_FORBIDDEN)

        product = self.get_object(pk)
        if not product:
            return Response({'error': 'Mahsulot topilmadi'}, status=status.HTTP_404_NOT_FOUND)

        product.delete()
        return Response({'msg': 'Mahsulot o‘chirildi'}, status=status.HTTP_204_NO_CONTENT)



