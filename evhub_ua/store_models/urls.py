from django.urls import path
from . import views

urlpatterns = [
    path('store/models/<str:category>/', views.ModelView.as_view(), name='models_page'),
    path('store/<str:category>/<str:model>/', views.ItemListPage.as_view(), name='constructor_page'),
]

htmx_urlpatterns = [
    path('store/<str:category>/', views.ItemsModel.as_view(), name='models_list'),
    path('models_constructor/', views.ModelsConstructorView.as_view(), name='constructor_results'),
    path('models_constructor/options', views.ConstructorOptionsView.as_view(), name='constructor_options'),

]

urlpatterns += htmx_urlpatterns