# Generated by Django 3.1.2 on 2021-12-24 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lerny', '0023_score_support_resource_support_resource_microlerny_lerny'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_lerny',
            name='access',
            field=models.BooleanField(default=True, verbose_name='is accessible?'),
        ),
        migrations.AlterField(
            model_name='support_resource',
            name='text',
            field=models.CharField(max_length=300, verbose_name='text '),
        ),
        migrations.AlterField(
            model_name='user_lerny',
            name='active',
            field=models.BooleanField(default=False, verbose_name='current status'),
        ),
    ]