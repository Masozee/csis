# Generated by Django 4.0.2 on 2022-06-18 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='order',
            field=models.PositiveIntegerField(blank=True, default=0),
            preserve_default=False,
        ),
    ]
