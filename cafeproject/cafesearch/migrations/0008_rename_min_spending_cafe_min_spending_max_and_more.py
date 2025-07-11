# Generated by Django 5.2.1 on 2025-05-26 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafesearch', '0007_tag_user_post'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cafe',
            old_name='min_spending',
            new_name='min_spending_max',
        ),
        migrations.AddField(
            model_name='cafe',
            name='district',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='cafe',
            name='min_spending_min',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
