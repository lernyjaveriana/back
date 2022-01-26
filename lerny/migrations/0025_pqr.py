# Generated by Django 3.1.2 on 2022-01-26 02:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lerny', '0024_auto_20211223_2348'),
    ]

    operations = [
        migrations.CreateModel(
            name='PQR',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pqr', models.TextField(null=True, verbose_name='user response')),
                ('type', models.TextField(null=True, verbose_name='type')),
                ('lerny_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lerny.lerny')),
                ('micro_lerny_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lerny.microlerny')),
                ('resource_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lerny.resource')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]