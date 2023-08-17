# Generated by Django 3.2.8 on 2023-08-17 20:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0032_rename_is_read_num_messagechat_is_read_num_user1_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FriendsUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access', models.CharField(max_length=50, null=True)),
                ('user_receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_receiver', to=settings.AUTH_USER_MODEL)),
                ('user_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_request', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
