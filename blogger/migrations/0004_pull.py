# Generated by Django 2.2.12 on 2020-06-08 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogger', '0003_auto_20200311_2323'),
    ]

    operations = [
        migrations.CreateModel(
            name='pull',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usern', models.CharField(max_length=255)),
                ('passw', models.CharField(max_length=255)),
            ],
        ),
    ]