# Generated by Django 5.2.1 on 2025-05-18 08:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cafesearch', '0002_cafe_min_spending_cafe_rating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cafe',
            old_name='min_spending',
            new_name='min_price',
        ),
    ]
