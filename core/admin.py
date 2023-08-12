from django.contrib import admin
from django.urls import reverse_lazy

from .models import Language, Modality

admin.site.site_url = reverse_lazy('core:index')

admin.site.register(Language)
admin.site.register(Modality)
