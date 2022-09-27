# Generated by Django 4.1 on 2022-09-27 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0006_postlike'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowersCnt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=50)),
                ('follower', models.IntegerField(default=0)),
            ],
        ),
    ]