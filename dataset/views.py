import base64
import json
import os
import tempfile
import zipfile

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files import File
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView
from PIL import Image

from core.models import Language, Modality
from dataset.models import Dataset, DatasetTag
from leaderboard.models import Entry
from model.models import Model

from .models import Dataset


class BaseDatasetView(LoginRequiredMixin):
	model = Dataset
	navigation = 'dataset'

class DatasetListView(BaseDatasetView, ListView):

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["lang_list"] = Language.objects.all()
		context["mod_list"]=Modality.objects.all()
		return context


class DatasetDetailView(BaseDatasetView, DetailView):
	pass


class DatasetVerifyView(DatasetDetailView):
	template_name = 'dataset/verify.html'

	def get_context_data(self, **kwargs):
		dataset = self.get_object()
		with open(dataset.file.path, 'r', encoding='utf-8') as f:
			kwargs.update({
				'word_list': json.loads(f.read())
			})
		return super().get_context_data(**kwargs)


def on_submit(request, id, lang, modality):
	mod = Model.objects.filter(language__name = lang.lower(),modality__name=modality.lower())
	f_ds = Dataset.objects.filter(id = id)
	a = Entry.objects.filter(dataset__name = f_ds[0])
	entry_ids = list(a.values_list('model_id', flat=True))
	model_ids = list(mod.values_list('id',flat = True))
	remaining_ids =[]
	for item in a.values():
		if(int(item['crr'])==0):
			remaining_ids.append(item['model_id'])
	for i in model_ids:
		if (i not in entry_ids):
			remaining_ids.append(i)
	remaining_ids = list(set(remaining_ids))
	final_mod = Model.objects.filter (id__in=remaining_ids)
	for i in range(len(final_mod)):
		new_entry,created = Entry.objects.get_or_create(model = final_mod[i], dataset = f_ds[0])
		new_entry.evaluate()
	return redirect('dataset:detail',pk=id)

def add_dataset(request):
	res =[]
	if(request.method == 'POST'): 
		form = request.POST
		
		name = request.POST.get('name')
		modality = form.get('modality').lower()
		if(len(Modality.objects.filter(name=modality))==0):
			messages.error(request,"Please enter a valid modality",extra_tags='alert')
			return redirect('dataset:list')
		modality_instance = Modality.objects.get(name=modality)
		language = form.get('language').lower()
		if(len(Language.objects.filter(name=language))==0):
			messages.error(request,"Please enter a valid Language",extra_tags='alert')
			return redirect('dataset:list')
		language_instance = Language.objects.get(name=language)
		description = form.get('description')
		tag_names = request.POST.getlist('tags')
		# print(request.FILES)
		uploaded_file = request.FILES['photo']
		# print(uploaded_file)

		details = Dataset.objects.all().values()
		for i in details:
			if((i['name']==form['name'])):
				lang_id = Language.objects.filter(name=language).values()[0]['id']
				mod_id =Modality.objects.filter(name=modality).values()[0]['id']

				if(i['modality_id']==mod_id and i['language_id']==lang_id):
					messages.warning(request,"Already exists in the database",extra_tags='alert')
					return redirect('dataset:list')
		tags = []
		for tag_name in tag_names:
			tag, created = DatasetTag.objects.get_or_create(name=tag_name)
			tags.append(tag)

		if uploaded_file.name.endswith('.zip'):
			entry=""
			target_folder = os.path.join('media', 'extracted_files')
			os.makedirs(target_folder, exist_ok=True)
			with tempfile.TemporaryDirectory(dir=target_folder) as temp_dir:
				# Combine the temporary directory path with a unique name for the extraction subfolder
				extract_folder = os.path.join(temp_dir, "extracted_contents")
				
				# Create the subdirectory for extraction
				os.makedirs(extract_folder)
				# Extract the contents of the zip file into the subdirectory
				with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
					# print(uploaded_file)
					zip_ref.extractall(extract_folder)
					# print("ok")
			

				temp_inner_folder = os.listdir(target_folder)[0]
				
				temp_inner_folder_path = os.path.join(target_folder ,temp_inner_folder)

				ec = os.listdir(temp_inner_folder_path)[0]

				ec_path = os.path.join(temp_inner_folder_path,ec)

				inner_folder = os.listdir(ec_path)[0]

				inner_folder_path = os.path.join(ec_path, inner_folder)
				
				gt_path = os.path.join(inner_folder_path ,os.listdir(inner_folder_path)[0])
				
				gt_dict = {}
				with open(gt_path ,'r', encoding='utf-8') as txt_file:
					txt = txt_file.readlines()
					for i in txt:
						a = i.split("\t")
						if len(a) >= 2:
							gt_dict[a[0]] = a[1]
						else:
							print("Line does not have enough elements:", a)
							messages.info(request,f"Line does not have enough elements:{a}")

				images_path = os.path.join(inner_folder_path ,os.listdir(inner_folder_path)[1])
				# print(os.listdir(images_path))
				
				
				for i in gt_dict:
					my_string = ''
					word=''
					pa = os.path.join(inner_folder_path, i)
					if (i.endswith('.jpg') or i.endswith('jpeg')):
							im = Image.open(pa)
							with open(pa, "rb") as img_file:
								binary_file_data = img_file.read()
								base64_encoded_data = base64.b64encode(binary_file_data)
								my_string = base64_encoded_data.decode('utf-8')
					else:
						messages.error(request,"Image does not end with .jpg")
					
					if (os.path.exists(pa)):
							word=gt_dict[i].strip()
					# print(my_string,word)
					res_dict = {"image":my_string, "gt":word}
					res.append(res_dict)
		# print(res)
		else:
			messages.error(request,"Only accepts files of the format, .zip")
			return redirect("dataset:list")
		dataset = Dataset(
            name=name,
            modality=modality_instance,
            language=language_instance,
            description=description,
        )
		dataset.save()
		dataset.tags.set(tags)	


		with open(name,'w') as json_file:
			json.dump(res,json_file)
		print(json_file)
		with open(name, 'rb') as json_file:
			dataset.file.save(f'{name}.json', File(json_file))	
		dataset.save()

		return redirect('dataset:list')
	
def delete_entry(request, entry_id, entry_model, dataset_id):
	delEntry = Entry.objects.filter(id=entry_id)
	delEntry.delete()
	messages.info(request, f'Entry with the name {entry_model} has been deleted',extra_tags='alert')
	return redirect('dataset:detail',pk=dataset_id)


