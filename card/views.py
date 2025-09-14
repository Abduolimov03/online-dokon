from django.shortcuts import render
from django.core.serializers import serialize
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from products.models import Product
from .serializers import CardSerializer, CardItemSerializer
from .models import Card, CardItem
from user_acc.user_perm import IsUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

# Create your views here.
