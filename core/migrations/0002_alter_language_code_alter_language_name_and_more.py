# Generated by Django 4.2 on 2023-04-28 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='language',
            name='code',
            field=models.CharField(default='', max_length=4, unique=True),
        ),
        migrations.AlterField(
            model_name='language',
            name='name',
            field=models.CharField(default='', max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='modality',
            name='name',
            field=models.CharField(default='', max_length=20, unique=True),
        ),
    ]
