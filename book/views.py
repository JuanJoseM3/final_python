from django.shortcuts import render
from book.permissions import IsLibraryUser, IsRentedToAnother
from .models import Book, BookItem
from rest_framework import viewsets, filters
from .serializers import CreateBookItemSerializer, BookSerializer, BookItemSerializer
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookItemViewSet(viewsets.ModelViewSet):
    queryset = BookItem.objects.all()
    serializer_class = BookItemSerializer
    permission_classes = [IsLibraryUser]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = [
        'book'
    ]
    search_fields = {
        'title',
        'subject',
        'author',
        'created_at'
    }

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return CreateBookItemSerializer
        else:
            return BookItemSerializer

    def get_permissions(self):
        if self.action == 'update':
            permissions = [IsRentedToAnother]
            return [permission() for permission in permissions]

        else:
            return [IsLibraryUser()]