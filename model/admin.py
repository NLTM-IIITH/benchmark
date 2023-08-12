from django.contrib import admin

from model.models import Model, ModelVersion

# Register your models here.

admin.site.register(Model)
admin.site.register(ModelVersion)
