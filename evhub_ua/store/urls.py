from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome_page, name='welcome_page'),
    path('store/', views.StorePageView.as_view(), name='store'),
    path('store/<str:category>/<str:model>/<slug:charger_slug>/', views.ItemDetail.as_view(), name='item_detail'),
]

htmx_urlpatterns = [
    path('search_results/', views.SearchResults.as_view(), name='search_results'),
    path('quick_view/<str:category>/<str:model>/<slug:charger_slug>/', views.QuickView.as_view(), name='quick_view'),
    path('contact_info/', views.contact_info, name='contact_info'),
]

urlpatterns += htmx_urlpatterns
