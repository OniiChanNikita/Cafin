# Generated by Django 4.2.3 on 2023-07-26 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0015_alter_operatingexpens_username'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='operatingexpens',
            managers=[
            ],
        ),
        migrations.AddField(
            model_name='financesettlement',
            name='percent_net_profit',
            field=models.IntegerField(null=True),
        ),
    ]