# Generated by Django 3.1.3 on 2020-12-02 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0003_auto_20201202_1946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='text',
            field=models.TextField(),
        ),
    ]
