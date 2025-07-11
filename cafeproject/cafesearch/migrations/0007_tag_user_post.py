# Generated by Django 5.2.1 on 2025-05-23 15:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafesearch', '0006_alter_cafe_latitude_alter_cafe_longitude'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=20)),
                ('enabled', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(default='請填寫暱稱', max_length=50)),
                ('cafe', models.CharField(default='請填寫咖啡廳名稱', max_length=50)),
                ('address', models.TextField(default='請填寫地址', max_length=50)),
                ('cafe_url', models.URLField(default='請填寫訂位網站連結', null=True)),
                ('del_pass', models.CharField(max_length=50)),
                ('pub_time', models.DateTimeField(auto_now=True)),
                ('enabled', models.BooleanField(default=False)),
                ('tags', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cafesearch.tag')),
            ],
        ),
    ]
