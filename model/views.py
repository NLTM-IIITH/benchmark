from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView

from .models import Model
from leaderboard.models import Entry
from dataset.models import Dataset

from django.shortcuts import render,redirect
from django.http import HttpResponse


class BaseModelView(LoginRequiredMixin):
	model = Model
	navigation = 'model'

class ModelListView(BaseModelView, ListView):
	pass

class ModelDetailView(BaseModelView, DetailView):
	pass

def on_submit(request , id , lang , modality):
	print(id,lang,modality)
	v_id = Model.objects.filter(id=id)[0]
	print(v_id.version)
	dataset_names = Dataset.objects.filter(language__name = lang.lower(), modality__name =modality.lower())
	print(dataset_names)
	a = Entry.objects.filter(model_id = id)
	print(a)
	entry_ids = list(a.values_list('dataset_id', flat=True))
	dataset_ids = list(dataset_names.values_list('id',flat = True))
	remaining_ids =[]
	for i in dataset_ids:
		if i not in entry_ids:
			remaining_ids.append(i)
	final_vals = Dataset.objects.filter (id__in=remaining_ids)
	for i in range(len(final_vals)):
		new_entry = Entry.objects.create(dataset = final_vals[i], model = v_id)
		new_entry.evaluate()
	return redirect('model:detail', pk=id)