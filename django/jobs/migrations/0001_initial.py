# Generated by Django 2.2.7 on 2019-11-20 12:41

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JobModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('job_class', models.CharField(max_length=200)),
                ('started', models.DateTimeField(blank=True, null=True)),
                ('finished', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[['Enqueued', 'Enqueued'], ['Started', 'Started'], ['Error', 'Error'], ['Executed', 'Executed']], default='Enqueued', max_length=50)),
                ('logs', models.TextField()),
                ('result_link', models.CharField(blank=True, default='', max_length=2000, null=True)),
            ],
        ),
    ]
