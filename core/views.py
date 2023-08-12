import json
import os
from datetime import datetime
from os.path import join
from typing import Any, Dict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage, default_storage
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, TemplateView

from model.models import Model


def save_file(location, file):
	if not os.path.exists(location):
		os.makedirs(location)
	fs = FileSystemStorage(location=location)
	fs.save(file.name, file)

@csrf_exempt
def ajoy_icdar_submission(request):
	path = '/home/krishna/ajoy_data/icdar'
	category = request.POST.get('category', 'default')
	if not category:
		category = 'default'
	path = join(path, category, str(datetime.now()))
	if not os.path.exists(path):
		os.makedirs(path)
	save_file(join(path, 'result'), request.FILES['result'])
	save_file(join(path, 'inference'), request.FILES['inference'])
	save_file(join(path, 'model'), request.FILES['model'])
	save_file(join(path, 'algorithm'), request.FILES['algorithm'])
	ret = {}
	ret['modeltext'] = request.POST.get('modeltext', '')
	ret['dataset'] = request.POST.get('dataset', '')
	ret['training'] = request.POST.get('training', '')
	ret['prepro'] = request.POST.get('prepro', '')
	ret['pospro'] = request.POST.get('pospro', '')
	with open(join(path, 'extra.json'), 'w', encoding='utf-8') as f:
		f.write(json.dumps(ret, indent=4))
	return redirect('https://ilocr.iiit.ac.in/ihtr/thanks.html')

@csrf_exempt
def ajoy_vqa_submission(request):
	path = '/home/krishna/ajoy_data/vqa'
	category = request.POST.get('category', 'default')
	if not category:
		category = 'default'
	path = join(path, category, str(datetime.now()))
	if not os.path.exists(path):
		os.makedirs(path)
	save_file(join(path, 'result'), request.FILES['result'])
	save_file(join(path, 'inference'), request.FILES['inference'])
	save_file(join(path, 'model'), request.FILES['model'])
	save_file(join(path, 'algorithm'), request.FILES['algorithm'])
	ret = {}
	ret['modeltext'] = request.POST.get('modeltext', '')
	ret['dataset'] = request.POST.get('dataset', '')
	ret['training'] = request.POST.get('training', '')
	ret['prepro'] = request.POST.get('prepro', '')
	ret['pospro'] = request.POST.get('pospro', '')
	with open(join(path, 'extra.json'), 'w', encoding='utf-8') as f:
		f.write(json.dumps(ret, indent=4))
	return redirect('https://ilocr.iiit.ac.in/ihtr/thanks.html')

class BaseCoreView:
	pass

class IndexView(BaseCoreView, ListView):
	template_name = 'core/index.html'
	navigation = 'index'
	model = Model


class LayoutAPIView(BaseCoreView, TemplateView):
	template_name = 'core/layout_api.html'
	navigation = 'api-layout'

class APIListView(BaseCoreView, ListView):
	template_name = 'core/modelapi.html'
	navigation = 'api-ocr'
	model = Model

	def get_context_data(self, **kwargs):
		kwargs.update({
			'language_list': [i[0] for i in list(Model.objects.values_list('language').distinct())]
		})
		return super().get_context_data(**kwargs)


class APIDetailView(BaseCoreView, TemplateView):
	template_name = 'core/modelapi_detail.html'
	navigation = 'api-ocr'
	
	def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
		language = self.request.GET.get('language', 'hindi')
		modality = self.request.GET.get('modality', 'printed')
		version = float(self.request.GET.get('version', 1))
		model = Model.objects.get(
			language=language,
			modality=modality,
			version=version,
		)
		ret = []
		try:
			path = '/home/krishna/leaderboard/core/static/core/samples/{}/{}'.format(
				model.modality,
				model.language,
			)
			static_path = '/bhashini-iiith/static/core/samples/{}/{}/'.format(
				model.modality,
				model.language,
			)
			a = open(os.path.join(path, 'v0.txt'), 'r').read().strip().split('\n')
			a = [i.strip() for i in a]
			for i in a:
				ret.append({
					'image': static_path + i.split(' ')[0].strip(),
					'ocrtext': i.split(' ')[1].strip(),
				})
		except Exception as e:
			print(e)
		kwargs.update({
			'model': model,
			'sample_list': ret,
		})
		return super().get_context_data(**kwargs)


class ModelAPIView(BaseCoreView, ListView):
	template_name = 'core/modelapi.html'
	navigation = 'index'
	model = Model


class ModelAPIDetailView(BaseCoreView, DetailView):
	template_name = 'core/modelapi_detail.html'
	navigation = 'index'
	model = Model

	def get_context_data(self, **kwargs):
		model = self.get_object()
		ret = []
		try:
			path = '/home/leaderboard/leaderboard/core/static/core/samples/{}/{}'.format(
				model.modality,
				model.language,
			)
			static_path = '/bhashini-iiith/static/core/samples/{}/{}/'.format(
				model.modality,
				model.language,
			)
			a = open(os.path.join(path, 'v0.txt'), 'r').read().strip().split('\n')
			a = [i.strip() for i in a]
			for i in a:
				ret.append({
					'image': static_path + i.split(' ')[0].strip(),
					'ocrtext': i.split(' ')[1].strip(),
				})
		except Exception as e:
			print(e)
		kwargs.update({
			'sample_list': ret
		})
		return super().get_context_data(**kwargs)
