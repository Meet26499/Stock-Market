# Generated by Django 3.2.21 on 2023-09-24 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_management', '0004_auto_20230924_1108'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='split_ratio',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]