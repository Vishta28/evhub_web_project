from store.models import ChargersItems
from store.views import get_all_images

class Cart(object):
	def __init__(self, request):
		print('init')
		self.session = request.session
		cart = self.session.get('cart')

		if not cart:
			self.session['cart'] = {}

		self.cart = cart

	def __iter__(self):
		print('iter start', self.cart)
		for slug in self.cart.keys():

			product = ChargersItems.objects.get(slug=slug)
			chargersitems_images = get_all_images(product)
			self.cart[slug]['product'] = product
			self.cart[slug]['image'] = chargersitems_images

		for item in self.cart.values():
			item['total_price'] = (item['product'].price * item['quantity'])
			print('iter end')

			yield item

	def total_cost(self):
		for slug in self.cart.keys():
			self.cart[slug]['product'] = ChargersItems.objects.get(slug=slug)
			print('total cost')

		return sum(item['product'].price * item['quantity'] for item in self.cart.values())


	def __len__(self):
		print('len')
		return sum(item['quantity'] for item in self.cart.values())


	def save(self):
		print('save')
		self.session['cart'] = self.cart
		self.session.modified = True

	def add(self, slug, quantity=1, update_quantity=False):
		print('add')

		if slug not in self.cart:
			self.cart[slug] = {'quantity': 1, 'slug': slug}
			print('slug cart', self.cart[slug])

		if update_quantity:
			self.cart[slug]['quantity'] += int(quantity)

			if self.cart[slug]['quantity'] == 0:
				self.remove(slug)

		self.save()

	def remove(self, slug):
		if slug in self.cart:
			del self.cart[slug]
			self.save()

		if not self.cart:
			del self.session['cart']
			self.session.modified = True

	# def remove_all(self):
	# 	del self.session['cart']
	# 	self.session.modified = True

	def get_item(self, slug):
		print('get item')
		if slug in self.cart:
			return self.cart[slug]
		else:
			return None
