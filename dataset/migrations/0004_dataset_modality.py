# Generated by Django 3.2.4 on 2023-02-06 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0003_alter_dataset_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='modality',
            field=models.CharField(choices=[('printed', 'Printed'), ('handwritten', 'Handwritten'), ('scenetext', 'Scene Text')], default='printed', max_length=20),
        ),
    ]