from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView

from .models import Dataset
from leaderboard.models import Entry
from dataset.models import Dataset
from model.models import Model

from django.shortcuts import render,redirect
from django.http import HttpResponse


class BaseDatasetView(LoginRequiredMixin):
	model = Dataset
	navigation = 'dataset'

class DatasetListView(BaseDatasetView, ListView):
    pass

	
    


class DatasetDetailView(BaseDatasetView, DetailView):


	# Below code can be used for sorting from backend. Use <a href="?order_by=crr">CRR (%)</a> in the frontend


	# model = Dataset
	# template_name = 'dataset/dataset_detail.html'
	# context_object_name = 'dataset'
	# def get_context_data(self, **kwargs):
	# 	context = super().get_context_data(**kwargs)
	# 	order_by = self.request.GET.get('order_by', 'defaultOrderField')
	# 	if(order_by == 'crr'):
	# 		items = Entry.objects.filter(dataset=context['dataset']).order_by('crr')
	# 	elif(order_by == 'wrr'):
	# 		items = Entry.objects.filter(dataset=context['dataset']).order_by('wrr')
	# 	else:
	# 		items = Entry.objects.filter(dataset=context['dataset']).order_by('?')

	# 	context['items'] = items
	# 	context['order_by'] = order_by
	# 	return context
	pass


def on_submit(request, id, lang, modality):
	mod = Model.objects.filter(language__name = lang.lower(),modality__name=modality.lower())
	f_ds = Dataset.objects.filter(id = id)
	a = Entry.objects.filter(dataset__name = f_ds[0])
	entry_ids = list(a.values_list('model_id', flat=True))
	model_ids = list(mod.values_list('id',flat = True))
	remaining_ids =[]
	for i in model_ids:
		if i not in entry_ids:
			remaining_ids.append(i)
	final_mod = Model.objects.filter (id__in=remaining_ids)
	for i in range(len(final_mod)):
		new_entry = Entry.objects.create(model = final_mod[i], dataset = f_ds[0])
		new_entry.evaluate()
	return redirect('dataset:detail',pk=id)


