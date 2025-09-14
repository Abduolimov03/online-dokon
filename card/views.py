from django.shortcuts import render
from django.core.serializers import serialize
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from products.models import Product
from .serializers import CardSerializer, CardItemSerializer
from .models import Card, CardItem
from user_acc.user_per import IsUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

# Create your views here.

class CardCreate(APIView):
    permission_classes = [IsUser, ]
    def post(self, request):
        card, created = Card.objects.get_or_create(user=request.user)
        serializer = CardSerializer(card)
        return Response({
            'data':serializer.data,
            "status":status.HTTP_201_CREATED if created else status.HTTP_200_OK
        })

class AddToCard(APIView):
    permission_classes = [IsUser, ]

    def post(self, request):
        product_id = request.data['product_id']
        ammount = int(request.data['ammount'])

        if not Product.objects.filter(id=product_id).exists():
            return Response({
                'error':'Siz mavjud bolmagan productni tanladingiz',
                'status':status.HTTP_400_BAD_REQUEST
            })
        if ammount <= 0 or ammount > 100:
            return Response({
                'error':'Siz xato malumot kiritdingiz',
                'status':status.HTTP_400_BAD_REQUEST
            })
        card, _ = Card.objects.get_or_create(user=request.user)
        product_obj = Product.objects.get(id=product_id)

        card_item = CardItem.objects.filter(card=card, product=product_obj).first()

        if card_item:
            card_item.ammount += ammount
            card_item.save()
        else:
            card_item = CardItem.objects.create(
                card = card,
                product = product_obj,
                ammount = ammount
            )

        serializer = CardItemSerializer(card_item)

        return Response({
            'data': serializer.data,
            'status': status.HTTP_201_CREATED
        })
