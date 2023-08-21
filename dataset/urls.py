from django.urls import path

from . import views

app_name = 'dataset'
urlpatterns = [
	path('', views.DatasetListView.as_view(), name='list'),
	path('<int:pk>/', views.DatasetDetailView.as_view(), name='detail'),
    path('on_submit/<int:id>/<str:lang>/<str:modality>', views.on_submit, name='on_submit'),
]
