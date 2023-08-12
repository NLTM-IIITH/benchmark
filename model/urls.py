from django.urls import path

from . import views

app_name = 'model'
urlpatterns = [
	path('', views.ModelListView.as_view(), name='list'),
	path('<int:pk>/', views.ModelDetailView.as_view(), name='detail'),
]
