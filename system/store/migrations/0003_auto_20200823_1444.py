# Generated by Django 3.0.7 on 2020-08-23 08:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='Quantity',
            new_name='quantity',
        ),
    ]
