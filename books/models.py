from django.db import models
class Category(models.Model):
    name = models.CharField(max_length=100)
       

class Book(models.Model):
    LANGUAGE_CHOICES = (
        ('EN', 'English'),
        ('HI', 'Hindi'),
    )

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    stock = models.IntegerField()
    cover_image = models.ImageField(upload_to='book_covers/', blank=True)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='EN') 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books', null=True, blank=True)


    def __str__(self):
        return f"{self.title} ({self.get_language_display()})"
from django.contrib.auth.models import User
from decimal import Decimal
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)  # snapshot of book price at purchase time

    def get_subtotal(self):
        return self.price * self.quantity