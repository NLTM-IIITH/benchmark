from django.urls import path

from . import views

app_name = 'leaderboard'
urlpatterns = [
	path('', views.LeaderboardListView.as_view(), name='list'),
	path('<int:pk>/', views.LeaderboardDetailView.as_view(), name='detail'),
]
