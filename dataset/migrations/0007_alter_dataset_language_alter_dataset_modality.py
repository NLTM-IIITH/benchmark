# Generated by Django 4.2 on 2023-04-26 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('dataset', '0006_auto_20230425_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='core.language'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='modality',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='core.modality'),
        ),
    ]