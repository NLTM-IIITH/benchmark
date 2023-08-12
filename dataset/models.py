from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse_lazy
from tqdm import tqdm

from core.models import BaseModel


class Dataset(BaseModel):
	
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
		return self.name

	def get_absolute_url(self):
		return reverse_lazy("dataset:detail", kwargs={"pk": self.pk})

	def get_tags(self) -> str:
		return ', '.join([str(i) for i in self.tags.all()])

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