from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView

from .models import Model


class BaseModelView(LoginRequiredMixin):
	model = Model
	navigation = 'model'

class ModelListView(BaseModelView, ListView):
	pass

class ModelDetailView(BaseModelView, DetailView):
	pass