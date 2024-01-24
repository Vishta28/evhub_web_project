from django.urls import path
from . import views

urlpatterns = [
    path('models_constructor/', views.ModelsConstructorView.as_view(), name='models_constructor'),
    path('models_constructor/options', views.ConstructorOptionsView.as_view(), name='constructor_options'),
]