from django.db import transaction
from rest_framework import serializers

from .models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    def validate_positions(self, positions):
        product_ids = [
            position['product'].pk
            for position in positions
        ]

        if len(product_ids) != len(set(product_ids)):
            raise serializers.ValidationError(
                'Товар не должен повторяться в списке позиций.'
            )

        return positions

    @transaction.atomic
    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)

        for position in positions:
            StockProduct.objects.create(
                stock=stock,
                **position,
            )

        return stock

    @transaction.atomic
    def update(self, instance, validated_data):
        positions = validated_data.pop('positions', None)
        stock = super().update(instance, validated_data)

        if positions is not None:
            for position in positions:
                StockProduct.objects.update_or_create(
                    stock=stock,
                    product=position['product'],
                    defaults={
                        'quantity': position['quantity'],
                        'price': position['price'],
                    },
                )

        return stock