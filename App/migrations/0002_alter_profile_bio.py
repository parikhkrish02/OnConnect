# Generated by Django 4.1 on 2022-09-26 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, default='Hey there, I am using OnConnect'),
        ),
    ]
