# Generated by Django 3.1.2 on 2021-07-26 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_user_points'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='points',
            field=models.FloatField(blank=True, null=True, verbose_name='points'),
        ),
    ]
