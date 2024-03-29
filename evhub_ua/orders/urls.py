from django.urls import path
from . import views
from orders.views import add_to_cart, header_menu_cart, update_cart, \
	cart_total, cart_items_total, CartAccessoriesView

urlpatterns = [
	path('cart', views.CartView.as_view(), name='cart'),
	path('add_to_cart/<slug:slug>/', add_to_cart, name='add_to_cart'),
	path('header_menu_cart', header_menu_cart, name='header_menu_cart'),
	path('update_cart/<slug:slug>/<str:action>/', update_cart, name='update_cart'),
	path('cart_total/', cart_total, name='cart_total'),
	path('cart_items_total/', cart_items_total, name='cart_items_total'),
	path('orders/order/', views.OrderView.as_view(), name='order'),
	path('orders/order_confirm/', views.ConfirmOrderView.as_view(), name='order_confirm'),
	path('orders/cart_accessories/<str:model>/', views.CartAccessoriesView.as_view(), name='cart_accessories')
]