# Generated by Django 4.2 on 2023-08-22 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaderboard', '0006_entry_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='description',
            field=models.TextField(default='No description available', help_text='Description of the model'),
        ),
    ]