# Generated by Django 3.1.3 on 2020-12-09 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0014_auto_20201209_1841'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='likes',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
