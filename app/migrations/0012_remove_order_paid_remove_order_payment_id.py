# Generated by Django 4.2.7 on 2024-12-10 11:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_order_paid_order_payment_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='paid',
        ),
        migrations.RemoveField(
            model_name='order',
            name='payment_id',
        ),
    ]
