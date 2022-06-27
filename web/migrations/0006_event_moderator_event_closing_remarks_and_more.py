# Generated by Django 4.0.2 on 2022-06-27 09:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_rename_pic_event_person_in_charge'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='Moderator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Moderator', to='web.person'),
        ),
        migrations.AddField(
            model_name='event',
            name='closing_remarks',
            field=models.ManyToManyField(related_name='ClosingSpeaker', to='web.Person'),
        ),
        migrations.AddField(
            model_name='event',
            name='opening_speech',
            field=models.ManyToManyField(related_name='OpeningSpeaker', to='web.Person'),
        ),
    ]
