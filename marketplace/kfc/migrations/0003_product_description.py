# Generated by Django 4.2.9 on 2024-03-02 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kfc', '0002_product_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(default=''),
        ),
    ]
