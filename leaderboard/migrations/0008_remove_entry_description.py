# Generated by Django 4.2 on 2023-08-22 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leaderboard', '0007_entry_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='description',
        ),
    ]