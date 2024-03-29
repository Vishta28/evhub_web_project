from django.shortcuts import render, get_object_or_404
from django_user_agents.utils import get_user_agent
from .models import ChargerItemModel, ChargersItems, Category, Accessories, AttachmentAccessories, Gallery
from django.views.generic import DetailView, ListView, TemplateView
from django.contrib.postgres.search import SearchQuery, SearchVector
from django.db.models import Q
from django.template.defaulttags import register
from .utils import get_first_image, get_all_images



class StoreFilter:
	def get_parameters(self):
		types = ChargersItems.objects.values_list('type', flat=True).distinct()
		powers_amps = ChargersItems.objects.values_list('power_amps', flat=True).distinct()
		brands = ChargersItems.objects.values_list('brand', flat=True).distinct()
		phases = ChargersItems.objects.values_list('phases', flat=True).distinct()
		categories = ChargersItems.objects.values_list('category', flat=True).distinct()
		return {'types': types, 'powers_amps': powers_amps, 'brands': brands, 'phases': phases, 'categories': categories}

# сторінка магазину з фільтрами


class StorePageView(ListView, StoreFilter):
	model = ChargersItems
	context_object_name = 'items'
	paginate_by = 4

	# підвантажуємо сторінку в залежності від типу притсрою

	def get_template_names(self, *args, **kwargs):
		user_agent = get_user_agent(self.request)
		if user_agent.is_mobile:
			return ['store/store_mob.html']
		elif user_agent.is_pc:
			return ['store/store.html']
		return super().get_template_names(*args, **kwargs)


	# Параметри для пагінації та фільтрації

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['categories'] = self.request.GET.get('categories', '')
		context['type'] = self.request.GET.get('type', '')
		context['power_amps'] = self.request.GET.get('power_amps', '')
		context['phases'] = self.request.GET.get('phases', '')
		context['brand'] = self.request.GET.get('brand', '')
		context['chargersitems_images'] = get_first_image(context)

		# отримуємо копію url видаляючи ключ page з url

		queries_without_page = self.request.GET.copy()
		if queries_without_page.get('page'):
			del queries_without_page['page']

		context['queries'] = queries_without_page.urlencode()

		return context

	# Фільтрація товарів на сторінці магазину

	def get_queryset(self, *args, **kwargs):

		qs = super().get_queryset(*args, **kwargs)

		# сортування товару (order_by)

		sorting_options = {
			'price_up': 'price',
			'price_down': '-price',
			'date_new': '-time',
			'in_stock': '-in_stock',
		}
		sort = self.request.GET.get('sort')
		if sort in sorting_options:
			sort_by = sorting_options[sort]
			sorted_queryset = ChargersItems.objects.order_by(sort_by)
			return sorted_queryset

		# Пошук товарів в стрчці пошуку в шапці сайту

		q = self.request.GET.get('q')

		if q:
			vector = SearchVector('title', 'category__title')
			query = SearchQuery(q)
			object_list = ChargersItems.objects.annotate(search=vector).filter(search=query)
			if object_list:
				return object_list
			else:
				return qs.filter(Q(title__icontains=q) | Q(category__title__icontains=q))

		# логіка фільтру на сторінці магазину

		filters = Q()

		categories_filters = Q()
		values = self.request.GET.getlist('categories')
		for value in values:
			if value:
				categories_filters |= Q(category=value)

		type_filters = Q()
		values = self.request.GET.getlist('type')
		for value in values:
			if value:
				type_filters |= Q(type=value)

		power_amps_filters = Q()
		values = self.request.GET.getlist('power_amps')
		for value in values:
			if value:
				power_amps_filters |= Q(power_amps=value)

		phases_filters = Q()
		phases_values = self.request.GET.getlist('phases')
		for value in phases_values:
			if value:
				phases_filters |= Q(phases=value)

		brand_filter = Q()
		value = self.request.GET.getlist('brand')
		for value in value:
			if value:
				brand_filter |= Q(brand=value)

		filters &= categories_filters
		filters &= type_filters
		filters &= power_amps_filters
		filters &= phases_filters
		filters &= brand_filter

		filtered_chargers = qs.filter(filters)

		return filtered_chargers

# детальна сторінка товару
class ItemDetail(DetailView):
	model = ChargersItems
	template_name = 'store/item_detail.html'
	slug_url_kwarg = 'charger_slug'
	context_object_name = 'item'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		print('context detail', context['item'])

		session_comparison = self.request.session.get('comparison')
		if session_comparison:
			item_exist_comparison = next((item for item in session_comparison if item['slug'] == context['item'].slug), None)
			context['item_exist_comparison'] = item_exist_comparison

		session_favorites = self.request.session.get('favorites')
		if session_favorites:
			item_exist_favorites = next((item for item in session_favorites if item['slug'] == context['item'].slug), None)
			context['item_exist_favorites'] = item_exist_favorites

		context['chargersitems_images'] = get_all_images(context)

		return context


class SearchResults(ListView):
	model = ChargersItems
	template_name = 'store/search_results.html'
	context_object_name = 'items'

	def get_queryset(self, *args, **kwargs):
		qs = super().get_queryset(*args, **kwargs)

		q = self.request.GET.get('q')

		if q:
			vector = SearchVector('title', 'category__title')
			query = SearchQuery(q)
			object_list = ChargersItems.objects.annotate(search=vector).filter(search=query)
			if object_list:
				return object_list
			else:
				return qs.filter(Q(title__icontains=q) | Q(category__title__icontains=q))

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['chargersitems_images'] = get_first_image(context)

		return context

class QuickView(DetailView):
	model = ChargersItems
	template_name = 'store/quick_view.html'
	context_object_name = 'item'
	slug_url_kwarg = 'charger_slug'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['chargersitems_images'] = get_all_images(context)

		return context

@register.filter
def get_item(dictionary, key):
	print(dictionary, key)
	print('here')
	return dictionary.get(key)


class AccessoriesStore(ListView):
	model = Accessories
	template_name = 'store/accessories_store.html'
	context_object_name = 'accessories'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		accessories = context['accessories']
		accessory_images = {}

		for accessory in accessories:
			# Отримати всі екземпляри AttachmentAccessories, які відповідають поточному аксесуару
			attachment_accessories = accessory.attachmentaccessories_set.all()
			# Припускається, що у моделі AttachmentAccessories є ForeignKey до моделі Gallery
			if attachment_accessories:
				accessory_images[accessory.slug] = [attachment_accessories.first().gallery.images.url]
			else:
				accessory_images[accessory.slug] = None
		context['accessory_images'] = accessory_images
		return context

# accessory_images[accessory.pk] = [attachment.gallery.images.url for attachment in attachment_accessories]
# accessory_images[accessory.pk] = attachment_accessories.first().gallery.images.url