# Generated by Django 3.0.2 on 2020-02-10 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0013_order_zipcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Started', 'Started'), ('Confirmed', 'Confirmed'), ('Started_Shipping', 'Started_Shipping'), ('Shipped', 'Shipped'), ('Abandoned', 'Abandoned'), ('Finished', 'Finished')], default='Started', max_length=120),
        ),
    ]
