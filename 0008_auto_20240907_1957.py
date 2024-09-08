# Generated by Django 3.2.8 on 2024-09-07 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0007_auto_20240907_1946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='location',
            field=models.CharField(default='Unknown', max_length=255),
        ),
        migrations.AlterField(
            model_name='job',
            name='company',
            field=models.CharField(default='Default Company', max_length=255),
        ),
        migrations.AlterField(
            model_name='job',
            name='location',
            field=models.CharField(default='Unknown', max_length=255),
        ),
    ]