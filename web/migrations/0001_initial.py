# Generated by Django 4.0.2 on 2022-06-27 05:43

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import embed_video.fields
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0004_alter_taggeditem_content_type_alter_taggeditem_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('slug', models.SlugField(default='', editable=False, max_length=320)),
                ('description', ckeditor.fields.RichTextField(blank=True)),
                ('image', models.ImageField(blank=True, upload_to='dept/')),
                ('image_credit', models.TextField(blank=True, null=True)),
                ('keterangan', models.TextField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('publish', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Department',
                'verbose_name_plural': 'Departments',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('slug', models.SlugField(default='', editable=False, max_length=320)),
                ('date_start', models.DateField()),
                ('date_end', models.DateField(blank=True, null=True)),
                ('location', models.CharField(blank=True, max_length=150, null=True)),
                ('image', models.ImageField(upload_to='event/img/')),
                ('file', models.FileField(blank=True, null=True, upload_to='event/file/')),
                ('link', models.URLField(blank=True)),
                ('youtube', embed_video.fields.EmbedVideoField()),
                ('description', ckeditor.fields.RichTextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('publish', models.BooleanField(default=False)),
                ('department', models.ManyToManyField(blank=True, to='web.Department')),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('slug', models.SlugField(default='', editable=False, max_length=160)),
                ('date_release', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('description', ckeditor.fields.RichTextField()),
                ('image', models.ImageField(upload_to='project/')),
                ('image_credit', models.TextField(blank=True, null=True)),
                ('publish', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'News',
                'verbose_name_plural': 'News',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('slug', models.SlugField(default='', editable=False, max_length=160)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='person/')),
                ('position', models.CharField(max_length=150)),
                ('organization', models.CharField(max_length=100)),
                ('category', models.CharField(choices=[('Scholar', 'Scholar'), ('Staff', 'Staff'), ('Foundation', 'Foundation'), ('Speaker', 'Speaker'), ('Colleague', 'Colleague')], max_length=10)),
                ('is_active', models.BooleanField()),
                ('description', ckeditor.fields.RichTextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('highlight', models.BooleanField(default=False)),
                ('order', models.PositiveIntegerField(blank=True)),
                ('twitter', models.URLField(blank=True, null=True)),
                ('facebook', models.URLField(blank=True, null=True)),
                ('linkedin', models.URLField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('department', models.ManyToManyField(blank=True, to='web.Department')),
            ],
            options={
                'verbose_name': 'People',
                'verbose_name_plural': 'Peoples',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('slug', models.SlugField(default='', editable=False, max_length=160)),
                ('description', ckeditor.fields.RichTextField()),
                ('image', models.ImageField(upload_to='project/')),
                ('periode_start', models.DateField(blank=True, null=True)),
                ('periode_end', models.DateField(blank=True, null=True)),
                ('publish', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('department', models.ManyToManyField(blank=True, to='web.Department')),
                ('project_member', models.ManyToManyField(to='web.Person')),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
            },
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('slug', models.SlugField(default='', editable=False, max_length=320)),
                ('date_publish', models.DateField(blank=True)),
                ('image', models.ImageField(upload_to='publication/')),
                ('image_credit', models.TextField(blank=True, null=True)),
                ('file', models.FileField(blank=True, upload_to='doc/')),
                ('description', ckeditor.fields.RichTextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('publish', models.BooleanField(default=False)),
                ('highlight', models.BooleanField(default=False)),
                ('authors', models.ManyToManyField(to='web.Person')),
            ],
            options={
                'verbose_name': 'Publication',
                'verbose_name_plural': 'Publications',
            },
        ),
        migrations.CreateModel(
            name='Publication_category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('slug', models.SlugField(default='', editable=False, max_length=200)),
                ('background', models.ImageField(blank=True, null=True, upload_to='pub_category/')),
                ('keterangan', models.TextField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Publication Category',
                'verbose_name_plural': 'Publication Categories',
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(default='', editable=False, max_length=320)),
                ('description', ckeditor.fields.RichTextField(blank=True)),
                ('image', models.ImageField(blank=True, upload_to='Topic/')),
                ('image_credit', models.TextField(blank=True, null=True)),
                ('keterangan', models.TextField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('publish', models.BooleanField(default=False)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.topic')),
            ],
            options={
                'verbose_name': 'Reseach Topic',
                'verbose_name_plural': 'Research Topic',
            },
        ),
        migrations.CreateModel(
            name='TaggedPublication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.publication')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_items', to='taggit.tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TaggedProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.project')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_items', to='taggit.tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TaggedNews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.news')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_items', to='taggit.tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TaggedEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.event')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_items', to='taggit.tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='publication',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.publication_category'),
        ),
        migrations.AddField(
            model_name='publication',
            name='department',
            field=models.ManyToManyField(blank=True, to='web.Department'),
        ),
        migrations.AddField(
            model_name='publication',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.project'),
        ),
        migrations.AddField(
            model_name='publication',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='web.TaggedPublication', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='publication',
            name='topic',
            field=models.ManyToManyField(blank=True, to='web.Topic'),
        ),
        migrations.AddField(
            model_name='project',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='web.TaggedProject', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='person',
            name='expertise',
            field=models.ManyToManyField(blank=True, to='web.Topic'),
        ),
        migrations.AddField(
            model_name='person',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='news',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='web.TaggedNews', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.CreateModel(
            name='Foundation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=100)),
                ('slug', models.SlugField(default='', editable=False, max_length=160)),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='project/')),
                ('publish', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('member', models.ManyToManyField(to='web.Person')),
            ],
            options={
                'verbose_name': 'BOD/Foundations',
                'verbose_name_plural': 'BOD/Foundations',
            },
        ),
        migrations.AddField(
            model_name='event',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.project'),
        ),
        migrations.AddField(
            model_name='event',
            name='speaker',
            field=models.ManyToManyField(blank=True, to='web.Person'),
        ),
        migrations.AddField(
            model_name='event',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='web.TaggedEvent', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='event',
            name='topic',
            field=models.ManyToManyField(blank=True, to='web.Topic'),
        ),
    ]
