# Generated by Django 3.2.4 on 2021-06-17 22:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lerny', '0010_company'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lerny_Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='date')),
                ('company_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lerny.company')),
                ('lerny_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lerny.lerny')),
            ],
        ),
    ]