# Generated by Django 3.1.2 on 2020-11-19 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='cellphone_number',
        ),
        migrations.RemoveField(
            model_name='user',
            name='passw',
        ),
        migrations.AddField(
            model_name='user',
            name='identification',
            field=models.CharField(default='12345', max_length=20, unique=True, verbose_name='identification'),
        ),
    ]
