from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('english/', views.english_books, name='english_books'),
    path('hindi/', views.hindi_books, name='hindi_books'),
    path('search/', views.search_books, name='search_books'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('add-to-cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('category/<int:category_id>/', views.books_by_category, name='books_by_category'),
    path('register/', views.register, name='register'),
    path('cart/remove/<int:book_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:book_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('confirm_order/', views.confirm_order, name='confirm_order'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('order/<int:order_id>/invoice/', views.download_invoice, name='download_invoice'),
    path('thank-you/', views.thank_you, name='thank_you'),


]
