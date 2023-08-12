from django.contrib import admin

from .models import Dataset, DatasetTag

admin.site.register(Dataset)
admin.site.register(DatasetTag)
