# Generated by Django 3.2.4 on 2023-02-03 17:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('model', '0003_rename_ame_modelversion_name'),
        ('dataset', '0003_alter_dataset_language'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('crr', models.FloatField(default=0.0, verbose_name='Character Recognition Rate')),
                ('wrr', models.FloatField(default=0.0, verbose_name='Word Recognition Rate')),
            ],
            options={
                'ordering': ['-created'],
                'default_related_name': 'evaluations',
            },
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='dataset.dataset')),
                ('evaluations', models.ManyToManyField(related_name='entries', to='leaderboard.Evaluation')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='model.model')),
            ],
            options={
                'default_related_name': 'entries',
            },
        ),
    ]
