# Generated by Django 4.0.2 on 2022-06-24 15:59

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_alter_publication_image_credit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
