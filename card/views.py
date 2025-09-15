from itertools import count

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


class CardItemUpdate(APIView):
    permission_classes = [IsUser, ]

    def post(self, request, pk):
        count = request.data.get('count', None)
        mtd = request.data.get('mtd', None)

        try:
            product = CardItem.objects.get(card__user=request.user, id=pk)
        except CardItem.DoesNotExist:
            return Response({'error':'Card Item topilmadi', 'status':status.HTTP_404_NOT_FOUND})
        if count is not None:
            product.ammount = int(count)
            product.save()
        elif mtd:
            if mtd == "+":
                product.ammount += 1
                product.save()
            elif mtd == "-":
                if product.ammount == 1:
                    product.delete()
                    return Response({
                        'msg':'Item ochirildi',
                        'status':status.HTTP_200_OK
                    })
                else:
                    product.ammount -= 1
                    product.save()
            else:
                return Response({'error':'Error', 'status':status.HTTP_400_BAD_REQUEST})

            serializer = CardItemSerializer(product)
            data = {
                'data':serializer.data,
                'status':status.HTTP_200_OK,
                'msg':'Ozgartirildi'
            }
            return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def card_detail(request):
    try:
        card = Card.objects.get(user = request.user)
    except Card.DoesNotExist:
        return Response({'msg':'Sizning savatingiz bosh', 'status':status.HTTP_404_NOT_FOUND})

    serializer = CardSerializer(card)
    return Response({'data':serializer.data, 'status':status.HTTP_200_OK})

@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def card_remove_item(request):
    product_id = Product.objects.get('product_id')
    if not product_id:
        return Response({'err':'product id kerak', 'status':status.HTTP_404_NOT_FOUND})

    try:
        card = Card.objects.get(user = request.user)
    except Card.DoesNotExist:
        return Response({'msg':'Savat topiladi', 'status':status.HTTP_404_NOT_FOUND})

    try:
        item = Card.objects.get(product_id=product_id)
        item.delete()
        return Response({'msg':'Mahsulot ochirildi', 'status':status.HTTP_200_OK})
    except CardItem.DoesNotExist:
        return Response({'msg':'Mahsulot savatda topilmadi', 'status':status.HTTP_404_NOT_FOUND})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def card_clear(request):
    try:
        card = Card.objects.get(user=request.user)
    except Card.DoesNotExist:
        return Response({'msg':'Savat topilmadi', 'status':status.HTTP_404_NOT_FOUND})

    card.item.all().delete()
    return Response({'msg':'savat tozalandi', 'status':status.HTTP_200_OK})





