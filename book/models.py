import uuid
from django.db import models
from core.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Author(models.Model):
    """
    Model representing the information of the author
    """

    name = models.CharField(max_length=80, blank=False, null=False)
    description = models.TextField()

    def __str__(self):
        return self.name

class Rack(models.Model):
    """
    Model representing information about the rack where the book is stored
    """

    location_identifier = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"Row: {self.location_identifier}"

class Book(models.Model):
    """
    Model representing the information of a book but not specificly a copy of the book
    """

    BOOK_SUBJECT_CHOICES = [
        ("li", "Literature"),
        ("hi", "History"),
        ("ma", "Mathematics"),
        ("ph", "Physics"),
        ("sc", "Science Fiction"),
        ("fi", "Philosophy"),
        ("dr", "Drama")
    ]

    LANGUAGE = [
        ("sp", "Spanish"),
        ("en", "English"),
        ("fr", "French"),
        ("it", "Italian"),
        ("jp", "Japanese")
    ]

    isbn = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=150)
    subject = models.CharField(choices=BOOK_SUBJECT_CHOICES, max_length=2)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    language = models.CharField(choices=LANGUAGE, max_length=2)
    number_of_pages = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title

class BookItem(models.Model):
    """
    Model representing a specific copy of each book which will be eventually rented by a member. Only a library can create, update or delete this book copies from the library.
    """

    barcode = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    due_date = models.PositiveSmallIntegerField('Number of days the book will be borrowed', default=5)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=False)
    rack = models.ForeignKey(Rack, on_delete=models.CASCADE, null=False)
    actual_owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    is_borrowed = models.BooleanField(default=False)
    is_reserved = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)

@receiver(post_save, sender=BookItem)
def update_availability(sender, instance, **kwargs):
    print(instance.is_borrowed)
    if not kwargs['created']:
        if instance.is_borrowed:
            is_available = False
        else:
            is_available = True

        BookItem.objects.filter(pk=instance.id).update(is_available=is_available)