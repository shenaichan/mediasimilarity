# Generated by Django 5.1.5 on 2025-01-31 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_trope_media'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trope',
            name='displayName',
            field=models.TextField(unique=True),
        ),
    ]
