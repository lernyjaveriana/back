# Generated by Django 3.1.2 on 2021-10-22 03:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lerny', '0021_auto_20211010_1851'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resource',
            name='content_url',
        ),
        migrations.RemoveField(
            model_name='resource',
            name='media_type',
        ),
        migrations.RemoveField(
            model_name='user_lerny',
            name='creation_date',
        ),
        migrations.RemoveField(
            model_name='user_lerny',
            name='last_view_date',
        ),
        migrations.RemoveField(
            model_name='user_lerny',
            name='lerny_points',
        ),
        migrations.RemoveField(
            model_name='user_lerny',
            name='opinion',
        ),
        migrations.RemoveField(
            model_name='user_lerny',
            name='opinion_points',
        ),
        migrations.RemoveField(
            model_name='user_lerny',
            name='pay_date',
        ),
        migrations.RemoveField(
            model_name='user_lerny',
            name='reference',
        ),
        migrations.RemoveField(
            model_name='user_lerny',
            name='valor',
        ),
    ]
