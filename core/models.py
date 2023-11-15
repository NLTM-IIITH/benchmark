from django.db import models


class BaseModel(models.Model):
	class Meta:
		abstract = True
	
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	def meta(self):
		return self._meta


class Language(BaseModel):
	code = models.CharField(
		default='',
		max_length=4,
		unique=True,
	)
	name = models.CharField(
		default='',
		max_length=20,
		unique=True,
	)

	def __str__(self) -> str:
		return self.name.title()

	def __repr__(self) -> str:
		return f'<Language: {str(self)}>'


class Modality(BaseModel):
	name = models.CharField(
		default='',
		max_length=20,
		unique=True,
	)

	def __str__(self) -> str:
		return self.name.title()

	def __repr__(self) -> str:
		return f'<Modality: {str(self)}>'

	@property
	def get_short_name(self) -> str:
		if self.name == 'printed':
			return 'p'
		elif self.name == 'handwritten':
			return 'hw'
		else:
			return 'st'