# Generated by Django 4.2.7 on 2024-12-09 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_remove_order_additional_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='postcode',
            field=models.IntegerField(null=True),
        ),
    ]