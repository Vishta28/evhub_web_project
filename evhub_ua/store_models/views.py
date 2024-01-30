from django.shortcuts import render, get_object_or_404
from django.views import View
from django_user_agents.utils import get_user_agent
from store.models import ChargerItemModel, ChargersItems, Category
from django.views.generic import DetailView, ListView, TemplateView
from django.contrib.postgres.search import SearchQuery, SearchVector
from django.db.models import Q

# сторінка де перелічені моделі товарів
class ModelView(TemplateView):
	template_name = 'store_models/models_page.html'

# сторінка котра підвантажує список моделей товарів за допомогою htmx
class ItemsModel(ListView):
	model = ChargerItemModel
	template_name = 'store_models/models_list.html'
	context_object_name = 'category_model'
	paginate_by = 3

	def get_queryset(self):
		category = self.kwargs.get('category')
		return ChargerItemModel.objects.filter(category__slug=category)

# сторінка товарів котрі відносяться до моделі виробу та фільтр конструктора
class ItemListPage(ListView):
	model = ChargersItems
	template_name = 'store_models/constructor_page.html'
	context_object_name = 'model_items'

	def get_queryset(self):
		item_model = self.kwargs.get('model')
		query = ChargersItems.objects.filter(model__slug=item_model)
		type = ChargersItems.objects.filter(model__slug=item_model).values('type').distinct()
		phases = ChargersItems.objects.filter(model__slug=item_model).values('phases').distinct()
		power_amps = ChargersItems.objects.filter(model__slug=item_model).values('power_amps').distinct()
		cable_length = ChargersItems.objects.filter(model__slug=item_model).values('cable_length').distinct()
		print(item_model)
		context = {
			'type': type,
			'phases': phases,
			'power_amps': power_amps,
			'cable_length': cable_length,
			'item_model': item_model,
			'query': query,
		}

		return context

class ModelsConstructorView(ListView):
	model = ChargersItems
	template_name = 'store_models/constructor_results.html'
	context_object_name = 'items_const'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		if context['items_const']:
			session_comparison = self.request.session.get('comparison')
			if session_comparison:
				item_exist_comparison = next(
					(item for item in session_comparison if item['slug'] == context['items_const'][0].slug), None)
				context['item_exist_comparison'] = item_exist_comparison

			session_favorites = self.request.session.get('favorites')
			if session_favorites:
				item_exist_favorites = next(
					(item for item in session_favorites if item['slug'] == context['items_const'][0].slug), None)
				context['item_exist_favorites'] = item_exist_favorites

		return context

	def get_queryset(self, *args, **kwargs):

		qs = super().get_queryset(*args, **kwargs)

		filters = Q()

		type_filters = Q()
		type = self.request.GET.get('type')
		if type:
			type_filters |= Q(type=type)

		power_amps_filters = Q()
		power_amps = self.request.GET.get('power_amps')
		if power_amps:
			power_amps_filters |= Q(power_amps=power_amps)

		phases_filters = Q()
		phases = self.request.GET.get('phases')
		if phases:
			phases_filters |= Q(phases=phases)

		cable_length_filters = Q()
		cable_length = self.request.GET.get('cable_length')
		if cable_length:
			cable_length_filters |= Q(cable_length=cable_length)

		model_filter = Q()
		model = self.request.GET.get('model')
		if model:
			model_filter |= Q(model__slug=model)

		filters &= type_filters
		filters &= power_amps_filters
		filters &= phases_filters
		filters &= cable_length_filters
		filters &= model_filter

		filtered_chargers = qs.filter(filters)

		return filtered_chargers

class ConstructorOptionsView(TemplateView):
	model = ChargersItems
	template_name = 'store_models/constructor_options.html'

	def get_context_data(self, **kwargs):
		context_type = self.request.GET.get('type', '')
		context_phases = self.request.GET.get('phases', '')
		return {'context_type': context_type, 'context_phases': context_phases}
