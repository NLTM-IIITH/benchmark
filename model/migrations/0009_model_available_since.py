# Generated by Django 4.2 on 2023-11-21 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0008_alter_modelversion_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='model',
            name='available_since',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]
