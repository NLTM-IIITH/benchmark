from django.db import models


class EntryQuerySet(models.QuerySet):
    def best_model(self, **kwargs):
        return 