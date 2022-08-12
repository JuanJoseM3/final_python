from rest_framework import serializers
from .models import Book, BookItem

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Book

class CreateBookSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Book

class ReadBookSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "author")
        model = Book

class MemberSerializer:
    class Meta:
        fields = "email, first_name"

class BookItemSerializer(serializers.ModelSerializer):
    book = ReadBookSerializer()
    member = MemberSerializer()
    class Meta:
        fields = "__all__"
        model = BookItem

class CreateBookItemSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = BookItem