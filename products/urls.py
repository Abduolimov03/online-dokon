from django.urls import path
from .views import ProductListApi, ProductUpdateDetailDeleteApi

urlpatterns = [
    path('products/', ProductListApi.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductUpdateDetailDeleteApi.as_view(), name='product-detail'),
]