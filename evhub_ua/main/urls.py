from django.urls import path
from . import views

urlpatterns = [
    path('active_buttons/', views.ActiveButtonsView.as_view(), name='active_buttons'),
]