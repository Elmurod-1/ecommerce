# Generated by Django 4.0.2 on 2022-05-09 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_productattribut_productattributvalue_stock_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productinventory',
            name='is_default',
            field=models.BooleanField(default=False, help_text='format: true=product visible', verbose_name='default '),
        ),
    ]