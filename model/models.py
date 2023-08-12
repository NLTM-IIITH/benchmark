from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse_lazy
from tqdm import tqdm

from core.models import BaseModel


class Model(BaseModel):
	version = models.ForeignKey(
		'model.ModelVersion',
		on_delete=models.RESTRICT,
	)
	language = models.ForeignKey(
		'core.Language',
		on_delete=models.RESTRICT,
	)
	modality = models.ForeignKey(
		'core.Modality',
		on_delete=models.RESTRICT,
	)

	class Meta:
		default_related_name = 'models'
		constraints = [
			models.UniqueConstraint(
				fields=['version', 'modality', 'language'],
				name='unique_version_modality_language'
			)
		]

	def __str__(self) -> str:
		return ' - '.join((
			str(self.modality),
			str(self.language),
			str(self.version)
		))

	def get_absolute_url(self):
		return reverse_lazy("model:detail", kwargs={"pk": self.pk})

	def populate_entries(self):
		# fetching all the dataset related models using language backdoor
		dataset_list = self.language.datasets.all()
		dataset_list = dataset_list.filter(modality=self.modality)
		for dataset in tqdm(dataset_list, desc='Populating the Entries model from Model'):
			self.entries.create(dataset=dataset) # type: ignore
	


class ModelVersion(BaseModel):
	name = models.CharField(
		default='',
		max_length=20,
		unique=True,
	)

	def __str__(self) -> str:
		return f'{self.name}'

	def __repr__(self) -> str:
		return f'<ModelVersion: {str(self)}>'


@receiver(post_save, sender=Model)
def populate_entries(sender, instance: Model, created: bool, **kwargs):
	if created:
		instance.populate_entries()