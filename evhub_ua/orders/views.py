from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView, ListView
from store.models import ChargersItems, Accessories
from .cart import Cart
from django_user_agents.utils import get_user_agent
from .forms import OrderForm
from .models import Order, OrderItem
from django.core.mail import send_mail
from store.views import get_first_image, get_all_images
from store.utils import get_all_imagesA, get_first_imageA
from django.template.defaulttags import register

# Create your views here.
class CartView(ListView):
	template_name = 'orders/cart.html'
	model = ChargersItems
	context_object_name = 'items'


def add_to_cart(request, slug):
	cart = Cart(request)
	cart.add(slug)

	return render(request, 'orders/partials/header_menu_cart_button.html')

def update_cart(request, slug, action):
	print('update_cart')
	cart = Cart(request)

	if action == 'increment':
		cart.add(slug, 1, True)
	elif action == 'decrement':
		cart.add(slug, -1, True)
	elif action == 'remove':
		cart.remove(slug)
	elif action == 'remove_all':
		cart.remove_all()


	product = ChargersItems.objects.get(slug=slug)
	quantity = cart.get_item(slug)
	chargersitems_images = get_all_images(product)

	if quantity:
		quantity = quantity['quantity']

		item = {
			'product': {
				'slug': product.slug,
				'title': product.title,
				'price': product.price,
				'model': product.model,
			},
			'total_price': (quantity * product.price),
			'quantity': quantity,
			'image': chargersitems_images,
		}
	else:
		item = None

	print(product.model)

	#правки правки правки
	user_agent = get_user_agent(request)
	if user_agent.is_mobile:
		response = render(request, 'orders/partials/cart_item_mob.html', {'item': item})
	else:
		response = render(request, 'orders/partials/cart_item.html', {'item': item})

	response['HX-Trigger'] = 'update_cart'

	return response


def header_menu_cart(request):
	return render(request, 'orders/partials/header_menu_cart_button.html')


def cart_total(request):
	return render(request, 'orders/partials/cart_total.html')


def cart_items_total(request):
	return render(request, 'orders/partials/cart_items_total.html')


class CartAccessoriesView(ListView):
	template_name = 'orders/cart_accessories.html'
	model = Accessories
	context_object_name = 'items'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		queryset = self.get_queryset()
		context['accessories_images'] = get_first_imageA(queryset)
		print(context['accessories_images'], 'context')

		return context

	def get_queryset(self, **kwargs):
		model = self.kwargs['model']
		qs = Accessories.objects.filter(chargeritem__title=model)
		return qs

# OrdersViews

class OrderView(TemplateView):
	template_name = 'orders/order.html'

	def get(self, request):
		form = OrderForm()
		return render(request, 'orders/order.html', context={'form': form})


class ConfirmOrderView(TemplateView):
	template_name = 'orders/order_confirm.html'

	def post(self, request):
		cart = Cart(request)
		session_key = request.session.session_key
		user = session_key
		first_name = request.POST.get('first_name')
		phone_number = request.POST.get('phone_number')
		total_cost = cart.total_cost()

		order = Order.objects.create(user=user, first_name=first_name, phone_number=phone_number, total_cost=total_cost)

		for item in cart:
			product = item['product']
			quantity = item['quantity']
			price = product.price * quantity

			print(price, product)

			order_item = OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)

		send_mail(
			subject='Замовлення',
			message=f'{first_name}\n{phone_number}\n{total_cost}',
			from_email='mailtrap@demomailtrap.com',
			recipient_list=['vishta28@gmail.com'],
		)

		cart = request.session.get('cart')
		if cart:
			del request.session['cart']
			request.session.modified = True

		return redirect('order_confirm')

