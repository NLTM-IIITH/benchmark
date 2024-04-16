from django.urls import path

from . import views

app_name = 'dataset'
urlpatterns = [
	path('', views.DatasetListView.as_view(), name='list'),
	path('add/', views.DatasetCreateView.as_view(), name='create'),
	path('<int:pk>/', views.DatasetDetailView.as_view(), name='detail'),
	path('<int:pk>/delete/', views.DatasetDeleteView.as_view(), name='delete'),
	path('<int:pk>/verify/', views.DatasetVerifyView.as_view(), name='verify'),
	path('on_submit/<int:id>/<str:lang>/<str:modality>', views.on_submit, name='on_submit'),
	path('add_dataset/', views.add_dataset, name='add_dataset'), # type: ignore
	path('delete_entry/<int:entry_id>/<str:entry_model>/<int:dataset_id>',views.delete_entry,name='delete_entry'),
	path('<int:pk>/report/', views.ReportView.as_view(), name='report'),
]
