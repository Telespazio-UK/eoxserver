# Generated by Django 3.2.12 on 2022-11-29 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coverages', '0011_bandstatistics'),
    ]

    operations = [
        migrations.AddField(
            model_name='browsetype',
            name='show_out_of_bounds_data',
            field=models.BooleanField(default=False),
        ),
    ]