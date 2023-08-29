from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView

from .models import Model, ModelVersion
from leaderboard.models import Entry
from dataset.models import Dataset
from core.models import Language,Modality

from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages

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

def add_model(request):
	if request.method == 'POST':
		modality = request.POST.get('modality').lower()

		if(len(Modality.objects.filter(name=modality))==0):
			messages.error(request,"Please enter a valid modality",extra_tags='alert')
			return redirect('model:list')
		
		modality_instance = Modality.objects.get(name=modality)
		language = request.POST.get('language').lower()
		if(len(Language.objects.filter(name=language))==0):
			messages.error(request,"Please enter a valid Language",extra_tags='alert')
			return redirect('model:list')
		language_instance = Language.objects.get(name=language)
		version = request.POST.get('version').lower()
		if(len(ModelVersion.objects.filter(name=version))==0):
			messages.error(request,"Please enter a valid version",extra_tags='alert')
			return redirect('model:list')
		version_instance = ModelVersion.objects.get(name=version)
		# print(language_instance,modality_instance,version_instance)
		obj = Model.objects.filter(language__name=language, modality__name=modality,version__name=version)
		if obj.count() == 0:
			model = Model(
				version = version_instance,
				language = language_instance,
				modality = modality_instance
			)
			model.save()
			messages.success(request,"Model Added",extra_tags='alert')
			return redirect('model:list')
		else:
			messages.error(request, 'This model already exists',extra_tags='alert')
			return redirect('model:list')  
		
		# return HttpResponse ('Model already exists. Please go back')

	