# Generated by Django 3.0.2 on 2020-02-15 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0018_auto_20200210_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='viewed',
            field=models.BooleanField(default=False),
        ),
    ]
