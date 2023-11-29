from django.shortcuts import render
from django_user_agents.utils import get_user_agent
from .models import ChargerItemModel, ChargersItems, Category
from django.views.generic import DetailView, ListView, TemplateView
from django.contrib.postgres.search import SearchQuery, SearchVector
from django.db.models import Q
from django.http import QueryDict
from urllib.parse import urlencode


class StoreFilter:
	def get_parameters(self):
		types = ChargersItems.objects.values_list('type', flat=True).distinct()
		powers_amps = ChargersItems.objects.values_list('power_amps', flat=True).distinct()
		brands = ChargersItems.objects.values_list('brand', flat=True).distinct()
		phases = ChargersItems.objects.values_list('phases', flat=True).distinct()
		categories = ChargersItems.objects.values_list('category', flat=True).distinct()
		return {'types': types, 'powers_amps': powers_amps, 'brands': brands, 'phases': phases, 'categories': categories}

# стартова сторінка
def welcome_page(request):
	user_agent = get_user_agent(request)
	if user_agent.is_mobile:
		return render(request, 'store/welcome_mob.html')
	else:
		return render(request, 'store/welcome.html')

# сторінка де перелічені моделі товарів
class ItemsModel(ListView):
	model = ChargerItemModel
	template_name = 'store/items_model.html'
	context_object_name = 'category_model'

	def get_queryset(self):
		category = self.kwargs.get('category')
		return ChargerItemModel.objects.filter(category__slug=category)

# сторінка товарів котрі відносяться до моделі виробу
class ItemListPage(ListView):
	model = ChargersItems
	template_name = 'store/items_list.html'
	context_object_name = 'items'

	def get_queryset(self):
		item_model = self.kwargs.get('model')
		return ChargersItems.objects.filter(model__slug=item_model)

# детальна сторінка товару
class ItemDetail(DetailView):
	model = ChargersItems
	template_name = 'store/item_detail.html'
	context_object_name = 'chargers_detail'
	slug_url_kwarg = 'charger_slug'


# сторінка магазину з фільтрами
class StorePageView(ListView, StoreFilter):
	model = ChargersItems
	context_object_name = 'items'
	paginate_by = 2

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
			'date_old': 'time'
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
				print(type_filters)

		print(type_filters)
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


class SearchResults(ListView):
	model = ChargersItems
	template_name = 'store/search_results.html'
	context_object_name = 'results'

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

class QuickView(DetailView):
	model = ChargersItems
	template_name = 'store/quick_view.html'
	context_object_name = 'chargers_detail'
	slug_url_kwarg = 'charger_slug'



