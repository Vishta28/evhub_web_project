from django.urls import path
from . import views

urlpatterns = [
    path('store/', views.StorePageView.as_view(), name='store'),
    path('store/<str:category>/<str:model>/<slug:charger_slug>/', views.ItemDetail.as_view(), name='item_detail'),
    path('store/accessories', views.AccessoriesStore.as_view(), name='store_accessories'),
]

htmx_urlpatterns = [
    path('search_results/', views.SearchResults.as_view(), name='search_results'),
    path('quick_view/<str:category>/<str:model>/<slug:charger_slug>/', views.QuickView.as_view(), name='quick_view'),
]

urlpatterns += htmx_urlpatterns
