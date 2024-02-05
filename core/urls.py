from django.urls import include, path

from . import views

app_name = 'core'
urlpatterns = [
	path('icdar/', views.ajoy_icdar_submission, name='icdar'),
	path('vqa/', views.ajoy_vqa_submission, name='vqa'),
	path('whatsapp/', views.whatsapp, name='whatsapp'),

	path('', views.IndexView.as_view(), name='index'),
	path('api/layout/', views.LayoutAPIView.as_view(), name='api-layout'),
	path('api/ocr/', views.APIListView.as_view(), name='api-list'),
	path('api/ocr/detail/', views.APIDetailView.as_view(), name='api-detail'),
	path('modelapi/', views.ModelAPIView.as_view(), name='modelapi'),
	path('modelapi/<int:pk>/', views.ModelAPIDetailView.as_view(), name='modelapi-detail'),
]
