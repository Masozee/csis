# Generated by Django 4.0.2 on 2022-03-22 09:58

from django.db import migrations
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_alter_event_date_end_project_event_project_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='youtube',
            field=embed_video.fields.EmbedVideoField(default=True),
            preserve_default=False,
        ),
    ]
