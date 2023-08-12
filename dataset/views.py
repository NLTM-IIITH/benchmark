from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView

from .models import Dataset


class BaseDatasetView(LoginRequiredMixin):
	model = Dataset
	navigation = 'dataset'

class DatasetListView(BaseDatasetView, ListView):
	pass

class DatasetDetailView(BaseDatasetView, DetailView):
	pass