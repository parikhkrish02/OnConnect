# Generated by Django 4.1 on 2022-09-26 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_alter_profile_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='proile_img',
            field=models.ImageField(default='blank-profile-picture.png', upload_to='profile_images'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, default='Hey there, I am using OnConnect !!!'),
        ),
    ]