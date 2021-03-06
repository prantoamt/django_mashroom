# Generated by Django 3.0.2 on 2020-02-02 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_code', models.CharField(default='', max_length=10, unique=True)),
                ('coupon_discount', models.DecimalField(decimal_places=2, default=0.0, max_digits=1000)),
                ('active', models.BooleanField(default=False)),
            ],
        ),
    ]
