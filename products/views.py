from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response

from products.models import Product
from products.serializers import ProductSerializer
from users.permissions import IsActiveEmployee


class ProductViewSet(viewsets.ViewSet):
    """ViewSet-класс для управления продуктами (создание, полное обновление, удаление)."""
    permission_classes = [IsActiveEmployee]

    def create(self, request):
        """Создание нового продукта."""
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        """Полное обновление существующего продукта."""
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Удаление существующего продукта."""
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
