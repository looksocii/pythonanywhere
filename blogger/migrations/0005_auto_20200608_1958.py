# Generated by Django 2.2.12 on 2020-06-08 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogger', '0004_pull'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pull',
            name='passw',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
