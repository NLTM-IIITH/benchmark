# Generated by Django 4.2 on 2024-04-15 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0011_dataset_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='collage_image',
            field=models.ImageField(blank=True, null=True, upload_to='Collages'),
        ),
    ]