from store.models import ChargerItemModel, ChargersItems, Category
from django.views.generic import DetailView, ListView, TemplateView, CreateView, View
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404

class FavoritesView(ListView):
	template_name = 'favorites/favorites.html'
	model = ChargersItems
	context_object_name = 'chargers_detail'

class AddToFavoritesView(View):
	def post(self, request):
		slug = request.POST.get('slug')

		# Отримуємо характеристики товару за допомогою slug
		charger_item = get_object_or_404(ChargersItems, slug=slug)

		# Якщо 'favorites' немає, то створ.ємо його як пустий список
		if request.session.get('favorites') is None:
			request.session['favorites'] = []
		else:
			request.session['favorites'] = list(request.session['favorites'])

		# Перевірка чи наявний товар у списку
		item_exist = next((item for item in request.session['favorites'] if item['slug'] == slug), None)

		# Якщо товар не в списку, то додаємо його slug та характеристики до списку favorites
		if not item_exist:
			request.session['favorites'].append({
				'slug': slug,
			})
			request.session.modified = True

		return redirect('favorites')

class DeleteFromFavoritesView(View):
	def post(self, request):
		slug = request.POST.get('slug')

		for item in request.session['favorites']:
			if item['slug'] == slug:
				item.clear()
				request.session.modified = True

		while {} in request.session['favorites']:
			request.session['favorites'].remove({})

		if not request.session['favorites']:
			del request.session['favorites']
			request.session.modified = True

		return redirect('favorites')

def favorite_button_active_view(request):
	return render(request, 'favorites/favorite_button_active.html')



