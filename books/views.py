from django.shortcuts import render
from django.shortcuts import render
from .models import Book
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from decimal import Decimal
from django.contrib import messages
from .models import Category
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth import login


def english_books(request):
    books = Book.objects.filter(language='EN')
    return render(request, 'books/english_books.html', {'books': books})

def hindi_books(request):
    books = Book.objects.filter(language='HI')
    return render(request, 'books/hindi_books.html', {'books': books})

def home(request):
    categories = Category.objects.all()
    return render(request, 'books/home.html', {'categories': categories})




def search_books(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )

    return render(request, 'books/search_results.html', {
        'query': query,
        'results': results
    })
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    print("Cart:", request.session.get('cart')) 
    return render(request, 'books/book_detail.html', {'book': book})
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart = request.session.get('cart', {})

    # Add or update the quantity
    if str(book_id) in cart:
        cart[str(book_id)] += 1
    else:
        cart[str(book_id)] = 1

    request.session['cart'] = cart  # Save cart to session
    return redirect('book_detail', book_id=book_id)

def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = Decimal('0.00')  # Initialize total price as Decimal for accuracy

    for book_id, quantity in cart.items():
        book = get_object_or_404(Book, pk=book_id)
        subtotal = book.price * quantity
        total_price += subtotal
        cart_items.append({
            'book': book,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return render(request, 'books/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })


def remove_from_cart(request, book_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})

        book_id_str = str(book_id)
        if book_id_str in cart:
            del cart[book_id_str]
            request.session['cart'] = cart  

    return redirect('view_cart')



def books_by_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    books = Book.objects.filter(category=category)
    return render(request, 'books/books_by_category.html', {
        'category': category,
        'books': books
    })
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
from django.shortcuts import redirect, get_object_or_404

def update_cart_quantity(request, book_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})

        # Make sure quantity is at least 1
        if quantity < 1:
            quantity = 1

        cart[str(book_id)] = quantity
        request.session['cart'] = cart

    return redirect('view_cart')
from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal
from .models import Book, Order, OrderItem

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return render(request, 'books/checkout.html', {'empty_cart': True})

    # On POST with simulate_payment flag
    if request.method == 'POST' and request.POST.get('simulate_payment') == 'true':
        # Save order as before
        order = Order.objects.create(user=request.user, total_price=sum(
            (get_object_or_404(Book, pk=book_id).price * qty) for book_id, qty in cart.items()
        ))
        for book_id, qty in cart.items():
            book = get_object_or_404(Book, pk=book_id)
            OrderItem.objects.create(order=order, book=book, quantity=qty, price=book.price)

        request.session['cart'] = {}  # Clear cart
        return redirect('thank_you')

    # On GET or no simulate flag, just render checkout summary
    cart_items = [...]
    total_price = ...
    return render(request, 'books/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'empty_cart': False
    })



@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'books/order_confirmation.html', {'order': order})
  


@login_required
def confirm_order(request):
    if request.method == 'POST':
        # Here you could save the order to the database later

        # Clear the cart session
        request.session['cart'] = {}

        return render(request, 'books/order_confirmation.html')

    # If GET request or other, redirect to home
    return redirect('home')
from .models import Order

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'books/my_orders.html', {'orders': orders})
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def download_invoice(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)

    # Create response as PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_order_{order.id}.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Helvetica", 12)

    y = 800
    p.drawString(100, y, f"Invoice for Order #{order.id}")
    p.drawString(100, y - 20, f"Date: {order.created_at.strftime('%Y-%m-%d %H:%M')}")
    p.drawString(100, y - 40, f"Customer: {order.user.username}")

    y -= 70
    p.drawString(100, y, "Items:")
from django.contrib.auth.decorators import login_required

@login_required
def thank_you(request):
    return render(request, 'books/thank_you.html')
