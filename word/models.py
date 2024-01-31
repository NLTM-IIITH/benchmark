from os.path import join

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from core.models import BaseModel

from .managers import WordQuerySet

User = get_user_model()


def get_image_path(instance, filename):
	return join(
		instance.category,
		instance.language,
		filename
	)

class Word(BaseModel):

	STATUS_CHOICES = (
		('new', 'New'),
		('correct', 'Correct'),
		('wrong', 'Wrong'),
		('skip', 'Skip'),
	)

	objects = WordQuerySet.as_manager()

	image = models.ImageField(
		verbose_name='Word Image',
		help_text='original word level cropped image',
		null=True,
		blank=True,
		upload_to=get_image_path,
	)

	status = models.CharField(
		max_length=10,
		choices=STATUS_CHOICES,
		default='new',
	)
	dataset = models.ForeignKey(
		'dataset.Dataset',
		on_delete=models.CASCADE,
	)
	user = models.ForeignKey(
		User,
		on_delete=models.SET_NULL,
		null=True,
		default=None,
		help_text='Indicates the user that verifies the word',
	)

	ocr = models.TextField(
		default='',
		help_text='This stores the OCR value of the word image'
	)

	verified_timestamp = models.DateTimeField(
		default=None,
		blank=True,
		null=True
	)

	class Meta:
		default_related_name = 'words'

	def __repr__(self) -> str:
		return f'<Word: {self.status}>'

	@property
	def is_verified(self) -> bool:
		"""
		Returns wheather this word is already verified or not?
		"""
		return self.status in [
			'correct',
			'wrong',
			'skip',
		]

	def verify(self, status: str, save: bool = True) -> None:
		"""
		Verifies the concerned word.
		its implied that Word.user has done the verification

		Effected Fields:
		 - Word.status
		 - Word.verified_timestamp
		"""
		self.status = status
		self.verified_timestamp = timezone.localtime()
		if save:
			self.save()

	def export(self):
		return {
			'id': self.id, # type: ignore
			'ocr': self.ocr.strip(),
			'status': self.status,
			'image': self.image.path.strip(),
		}