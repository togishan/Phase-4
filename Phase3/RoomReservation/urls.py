from django.urls import path, include
from . import views

urlpatterns = [
	path('', views.index, name='index'),
    path('accounts/register/', views.RegistrationView.as_view(), name='registration'),
]