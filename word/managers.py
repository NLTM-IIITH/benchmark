import os
from os.path import join

from django.contrib.auth import get_user_model
from tqdm import tqdm

from core.managers import BaseQuerySet

User = get_user_model()


class WordQuerySet(BaseQuerySet):

	def verified(self, **kwargs):
		return self.filter(
			status='correct',
			**kwargs
		)

	def save_images(self, folder_path: str):
		for word in tqdm(self.all(), desc='Saving images'):
			out_path = join(folder_path, f'{word.id}.jpg')
			os.system(f'cp {word.image.path} {out_path}')

	def remove_verify(self) -> None:
		"""
		Removes the verified status for all the words.

		Effected Fields:
		 - Word.status
		"""
		self.all().update(
			status='new'
		)

	def refresh(self):
		ids = self.all().values_list('id', flat=True)
		return self.model.objects.filter(id__in=ids)
