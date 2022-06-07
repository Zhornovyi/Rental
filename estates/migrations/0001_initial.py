# Generated by Django 2.2.2 on 2022-06-06 10:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import estates.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EstatePost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_title', models.CharField(blank=True, max_length=100)),
                ('description', models.TextField(blank=True, max_length=5000)),
                ('city', models.CharField(blank=True, max_length=120)),
                ('address', models.TextField(blank=True, max_length=500)),
                ('price', models.IntegerField(blank=True, default=0)),
                ('square_meters', models.IntegerField(blank=True, default=0)),
                ('type', models.CharField(blank=True, max_length=100)),
                ('floor', models.IntegerField(blank=True, null=True)),
                ('proof_doc', models.FileField(blank=True, upload_to=estates.models.upload_location)),
                ('image', models.ImageField(blank=True, upload_to=estates.models.upload_location)),
                ('contracted', models.BooleanField(blank=True, default=False)),
                ('date_published', models.DateTimeField(auto_now_add=True, verbose_name='date published')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='date updated')),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'estates_posts',
            },
        ),
        migrations.CreateModel(
            name='EstateReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=5000)),
                ('rate', models.IntegerField()),
                ('date_published', models.DateTimeField(auto_now_add=True, verbose_name='date published')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('estate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='estates.EstatePost')),
            ],
            options={
                'db_table': 'estate_reviews ',
            },
        ),
    ]