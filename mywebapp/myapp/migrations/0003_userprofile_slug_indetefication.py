# Generated by Django 4.2.3 on 2023-07-24 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='slug_indetefication',
            field=models.SlugField(null=True, unique=True),
        ),
    ]
