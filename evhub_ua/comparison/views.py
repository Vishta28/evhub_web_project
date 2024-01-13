from django.shortcuts import render, redirect
from django.views.generic import DetailView, TemplateView, ListView

from store.models import ChargersItems


class ComparisonView(ListView):
	template_name = 'comparison/comparison_page.html'
	model = ChargersItems
	context_object_name = 'chargers_detail'

class AddToComparisonView(DetailView):
	def post(self, request):
		slug = request.POST.get('slug')

		# Отримуємо характеристики товару за допомогою slug

		# Якщо 'favorites' немає, то створ.ємо його як пустий список
		if request.session.get('comparison') is None:
			request.session['comparison'] = []
		else:
			request.session['comparison'] = list(request.session['comparison'])

		request.session['comparison'].append({
			'slug': slug,
		})
		request.session.modified = True
		print(request.session['comparison'])

		return redirect('comparison')

class DeleteFromComparisonView(DetailView):
	def post(self, request):
		slug = request.POST.get('slug')

		for item in request.session['comparison']:
			if item['slug'] == slug:
				item.clear()
				request.session.modified = True

		while {} in request.session['comparison']:
			request.session['comparison'].remove({})

		if not request.session['comparison']:
			del request.session['comparison']
			request.session.modified = True

		return redirect('comparison')
