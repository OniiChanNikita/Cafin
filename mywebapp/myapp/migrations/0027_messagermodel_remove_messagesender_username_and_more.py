# Generated by Django 4.2.3 on 2023-07-29 08:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0026_alter_messagechat_user1_search_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessagerModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='messagesender',
            name='username',
        ),
        migrations.RemoveField(
            model_name='messagechat',
            name='user2',
        ),
        migrations.DeleteModel(
            name='MessageRecipient',
        ),
        migrations.DeleteModel(
            name='MessageSender',
        ),
        migrations.AlterField(
            model_name='messagechat',
            name='user1',
            field=models.ManyToManyField(to='myapp.messagermodel'),
        ),
    ]