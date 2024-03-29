# Generated by Django 3.1.2 on 2021-09-27 12:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lerny', '0019_auto_20210921_1233'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Group_name', models.CharField(max_length=50, verbose_name='group name')),
                ('lerny_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lerny.lerny')),
            ],
        ),
        migrations.CreateModel(
            name='User_Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Group_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lerny.group')),
                ('User_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
