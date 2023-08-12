import json
import time
from os.path import basename, join
from tempfile import TemporaryDirectory

from django.core.files import File
from django.core.validators import (FileExtensionValidator, MaxValueValidator,
                                    MinValueValidator)
from django.db import models
from django.urls import reverse_lazy
from nltk.metrics.distance import edit_distance

from api.ocr import OCRAPI
from core.models import BaseModel


class Entry(BaseModel):
	"""
	This is a main model to store a single Leaderboard Entry
	"""
	model = models.ForeignKey(
		'model.Model',
		on_delete=models.CASCADE,
	)
	dataset = models.ForeignKey(
		'dataset.Dataset',
		on_delete=models.CASCADE,
	)
	crr = models.FloatField(
		verbose_name='CRR',
		help_text='Character Recognition Rate',
		default=0.0,
		validators=[
			MaxValueValidator(100.0),
			MinValueValidator(0.0),
		],
	)
	wrr = models.FloatField(
		verbose_name='WRR',
		help_text='Word Recognition Rate',
		default=0.0,
		validators=[
			MaxValueValidator(100.0),
			MinValueValidator(0.0),
		],
	)
	file = models.FileField(
		null=True,
		blank=True,
		verbose_name='JSON File',
		help_text=(
			'This field accepts the test images and thier groundtruth '
			'in the correct format.'
			'The JSON file will contain a list of dicts with each dict '
			'having "gt" key that will store the GT of that image and "ocr" '
			'key that will store the ocr text of the image'
		),
		upload_to='Benchmarks',
		validators=[
			FileExtensionValidator(['json'])
		]
	)

	class Meta:
		default_related_name = 'entries'
		ordering = ['-created']
		constraints = [
			models.UniqueConstraint(
				fields=['model', 'dataset'],
				name='unique_model_dataset'
			)
		]

	def get_absolute_url(self):
		return reverse_lazy("leaderboard:detail", kwargs={"pk": self.pk})

	def infer_ocr(self) -> list[dict[str, str]]:
		"""
		A function to call the OCRAPI for this particular
		dataset and model
		"""
		return OCRAPI.fire(
			self.dataset,
			self.model
		)

	def format_data(self, data: list[dict[str, str]], tmp) -> str:
		with open(self.dataset.file.path, 'r', encoding='utf-8') as f:
			dataset = json.loads(f.read().strip())
		ret = []
		for d,dt in zip(data, dataset):
			ret.append({
				'image': dt['image'],
				**d
			})
		path = join(tmp.name, f'{self.id}.json') # type: ignore
		with open(path, 'w', encoding='utf-8') as f:
			f.write(json.dumps(ret, indent=4))
		return path

	def evaluate(self):
		"""
		input is in the same format as outputted by the OCRAPI
		and output is in the format
		{
			"crr": 33.23,
			"wrr": 66.12
		}
		"""
		t = time.time()
		try:
			data = self.infer_ocr()
		except:
			print('Error while performing OCR')
			return None
		print(f'Completed the OCR Inference in {time.time()-t} seconds')
		cer = []
		wrr = []
		for i in data:
			wrr.append(1 if i['ocr']==i['gt'] else 0)
			if len(i['gt']) == 0:
				cer.append(0)
			else:
				cer.append(edit_distance(i['gt'], i['ocr'])/len(i['gt']))
		self.crr = round(100-sum(cer)*100/len(cer), 2)
		self.wrr = round(sum(wrr)*100/len(wrr), 2)
		tmp = TemporaryDirectory(prefix='json')
		path = self.format_data(data, tmp)
		self.file.save(
			basename(path),
			File(open(path, 'rb')),
			save=False
		)
		self.save()