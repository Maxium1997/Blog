# Generated by Django 3.1.2 on 2020-11-15 03:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0005_auto_20201115_0342'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='boxes',
        ),
        migrations.AddField(
            model_name='tag',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
