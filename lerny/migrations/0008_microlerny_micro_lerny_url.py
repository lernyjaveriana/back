# Generated by Django 3.1.2 on 2020-11-25 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lerny', '0007_auto_20201124_2218'),
    ]

    operations = [
        migrations.AddField(
            model_name='microlerny',
            name='micro_lerny_url',
            field=models.CharField(default='eeee', max_length=300, verbose_name='microlerny url'),
            preserve_default=False,
        ),
    ]
