import base64
import json
import os
import zipfile
from os.path import basename, join
from tempfile import TemporaryDirectory

from django.core.files import File
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse_lazy
from tqdm import tqdm

from core.models import BaseModel, Language, Modality
from word.models import Word


class Dataset(BaseModel):
	description = models.TextField(
		default='No description available',
		help_text='Description of the model',
	)
	name = models.CharField(
		max_length=100,
		default='',
		blank=True,
	)
	language = models.ForeignKey(
		'core.Language',
		on_delete=models.RESTRICT,
	)
	modality = models.ForeignKey(
		'core.Modality',
		on_delete=models.RESTRICT,
	)
	tags = models.ManyToManyField(
		'dataset.DatasetTag',
		related_name='datasets',
	)
	version = models.IntegerField(default=1)
	file = models.FileField(
		null=True,
		blank=True,
		verbose_name='JSON File',
		help_text=(
			'This field accepts the test images and thier groundtruth '
			'in the correct format.'
			'The JSON file will contain a list of dicts with each dict '
			'having "image" key with base64 encoded image and "gt" key '
			'that will store the GT of that image.'
		),
		upload_to='Datasets',
		validators=[
			FileExtensionValidator(['json'])
		]
	)

	class Meta:
		default_related_name = 'datasets'

	def __str__(self) -> str:
		return 'BM-{}-{}-{}'.format(
			self.modality.get_short_name.upper(),
			self.language.code.upper(),
			self.version,
		)

	def populate_word_model(self):
		with open(self.file.path, 'r', encoding='utf-8') as f:
			words = json.loads(f.read())
		if self.words.count() == len(words): # type: ignore
			return None
		print(f'Creating {len(words)} word model instances')
		tmp = TemporaryDirectory()
		word_list = []
		for i, v in tqdm(enumerate(words)):
			img_path = join(tmp.name, f'{i}.jpg')
			with open(img_path, 'wb') as f:
				f.write(base64.b64decode(v['image']))
			w = Word(ocr=v['gt'], dataset=self)
			w.image.save(
				basename(img_path),
				File(open(img_path, 'rb')),
				save=False
			)
			word_list.append(w)
		Word.objects.bulk_create(word_list)

	def get_absolute_url(self):
		return reverse_lazy("dataset:detail", kwargs={"pk": self.pk})

	def get_verify_url(self):
		return reverse_lazy('dataset:verify', kwargs={'pk': self.pk})

	def get_tags(self) -> str:
		return ', '.join([str(i) for i in self.tags.all()])

	@staticmethod
	def from_ajoy_style_gt(path: str, name, modality, language):
		modality = Modality.objects.get(name=modality.lower().strip())
		language = Language.objects.get(name=language.lower().strip())

		target_folder = join('media', 'extracted_files')
		os.makedirs(target_folder, exist_ok=True)
		res = []
		with TemporaryDirectory(dir=target_folder) as temp_dir:
			# Combine the temporary directory path with a unique name for the extraction subfolder
			extract_folder = join(temp_dir, "extracted_contents")
			
			# Create the subdirectory for extraction
			os.makedirs(extract_folder)
			# Extract the contents of the zip file into the subdirectory
			with zipfile.ZipFile(path, 'r') as zip_ref:
				zip_ref.extractall(extract_folder)

			temp_inner_folder = os.listdir(target_folder)[0]
			temp_inner_folder_path = join(target_folder ,temp_inner_folder)

			ec = os.listdir(temp_inner_folder_path)[0]
			ec_path = join(temp_inner_folder_path,ec)

			inner_folder = os.listdir(ec_path)[0]
			inner_folder_path = join(ec_path, inner_folder)
			
			gt_path = join(inner_folder_path ,os.listdir(inner_folder_path)[0])
			
			gt_dict = {}
			with open(gt_path ,'r', encoding='utf-8') as txt_file:
				txt = txt_file.readlines()
				for i in txt:
					a = i.split("\t")
					if len(a) >= 2:
						gt_dict[a[0]] = a[1]
					else:
						print("Line does not have enough elements:", a)
			for i in tqdm(gt_dict):
				my_string = ''
				word=''
				pa = join(inner_folder_path, i)
				if (i.endswith('.jpg') or i.endswith('jpeg')):
						with open(pa, "rb") as img_file:
							binary_file_data = img_file.read()
							base64_encoded_data = base64.b64encode(binary_file_data)
							my_string = base64_encoded_data.decode('utf-8')
				else:
					print('Image does not end with .jpg')
				
				if (os.path.exists(pa)):
						word=gt_dict[i].strip()
				res_dict = {"image":my_string, "gt":word}
				res.append(res_dict)
		dataset = Dataset(
            name=name,
            modality=modality,
            language=language,
            description='',
        )
		dataset.save()

		with open(name,'w') as json_file:
			json.dump(res,json_file, indent=4)
		with open(name, 'rb') as json_file:
			dataset.file.save(f'{name}.json', File(json_file))	
		dataset.save()

	def populate_entries(self, **kwargs):
		# fetching all the model related models using language backdoor
		model_list = self.language.models.all()
		model_list = model_list.filter(modality=self.modality, **kwargs)
		for model in tqdm(model_list, desc='Populating the Entries model from Dataset'):
			self.entries.create(model=model) # type: ignore
	

class DatasetTag(BaseModel):
	name = models.CharField(
		default='',
		max_length=50,
		unique=True,
	)

	def __str__(self) -> str:
		return self.name

	def __repr__(self) -> str:
		return f'<DatasetTag: {str(self)}>'


@receiver(post_save, sender=Dataset)
def populate_entries(sender, instance: Dataset, created: bool, **kwargs):
	if created:
		instance.populate_entries()