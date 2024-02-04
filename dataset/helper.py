
import base64
import json
import os
import tempfile
import zipfile

from django.core.files import File

from core.models import Language, Modality

from .models import Dataset


def from_zip_path(path, language, modality, version, description):
	res = []
	if not os.path.exists(path) or not path.endswith('zip'):
		print('invalid path')
		return None
	name = f'{modality}_{language}_{version}'

	try:
		modality_instance = Modality.objects.get(name=modality)
	except:
		print('modality error')
		return
	try:
		language_instance = Language.objects.get(name=language)
	except:
		print('language error')
		return

	if Dataset.objects.filter(
		modality=modality_instance,
		language=language_instance,
		version=version
	).exists():
		print('already exist')
		return

	target_folder = os.path.join('media', 'extracted_files')
	os.makedirs(target_folder, exist_ok=True)
	with tempfile.TemporaryDirectory(dir=target_folder) as temp_dir:
		# Combine the temporary directory path with a unique name for the extraction subfolder
		extract_folder = os.path.join(temp_dir, "extracted_contents")
		
		# Create the subdirectory for extraction
		os.makedirs(extract_folder)
		# Extract the contents of the zip file into the subdirectory
		with zipfile.ZipFile(path, 'r') as zip_ref:
			zip_ref.extractall(extract_folder)

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
		for i in gt_dict:
			try:
				my_string = ''
				word=''
				pa = os.path.join(inner_folder_path, i)
				if i.endswith('.jpg') or i.endswith('jpeg'):
					with open(pa, "rb") as img_file:
						binary_file_data = img_file.read()
						base64_encoded_data = base64.b64encode(binary_file_data)
						my_string = base64_encoded_data.decode('utf-8')
				else:
					print("Image does not end with .jpg")
			
				if os.path.exists(pa):
					word=gt_dict[i].strip()

				res_dict = {"image":my_string, "gt":word}
			except:
				continue
			res.append(res_dict)
	dataset = Dataset( name=name, modality=modality_instance, language=language_instance, description=description, version=version)
	dataset.save()


	with open(name,'w') as json_file:
		json.dump(res,json_file, indent=4)
	with open(name, 'rb') as json_file:
		dataset.file.save(f'{name}.json', File(json_file))	
	dataset.save()
	dataset.populate_word_model()