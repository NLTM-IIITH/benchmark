# Generated by Django 3.2.4 on 2023-02-03 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DatasetTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(default='', max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, default='', max_length=100)),
                ('version', models.IntegerField(default=1)),
                ('file', models.FileField(blank=True, help_text='This field accepts the test images and thier groundtruth in the correct format.', null=True, upload_to='Datasets', verbose_name='JSON File')),
                ('tags', models.ManyToManyField(related_name='datasets', to='dataset.DatasetTag')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
