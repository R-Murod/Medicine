# Generated by Django 3.1.7 on 2023-04-24 13:15

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
                ('logo_icon', models.CharField(blank=True, max_length=200)),
                ('text', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
                ('profession', models.CharField(blank=True, max_length=200)),
                ('logo', models.ImageField(blank=True, upload_to='upload')),
                ('twitter', models.CharField(blank=True, max_length=200)),
                ('whatsapp', models.CharField(blank=True, max_length=200)),
                ('facebook', models.CharField(blank=True, max_length=200)),
                ('instagram', models.CharField(blank=True, max_length=200)),
                ('desc', models.CharField(blank=True, max_length=200)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.category')),
            ],
        ),
        migrations.CreateModel(
            name='SiteUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(blank=True, max_length=200)),
                ('first_name', models.CharField(blank=True, max_length=200)),
                ('middle_name', models.CharField(blank=True, max_length=200)),
                ('iin', models.CharField(blank=True, max_length=200)),
                ('phone', models.CharField(blank=True, max_length=200)),
                ('email', models.CharField(blank=True, max_length=200)),
                ('password', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mini_desc', models.CharField(blank=True, max_length=200)),
                ('desc', models.CharField(blank=True, max_length=200)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.category')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(blank=True, max_length=200)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category', to='main.category')),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200)),
                ('posted_date', models.DateTimeField(default=datetime.datetime(2023, 4, 24, 19, 15, 47, 867625))),
                ('logo', models.ImageField(blank=True, upload_to='upload')),
                ('logo1', models.ImageField(blank=True, upload_to='upload')),
                ('desc1', models.CharField(blank=True, max_length=200)),
                ('desc2', models.CharField(blank=True, max_length=200)),
                ('desc3', models.CharField(blank=True, max_length=200)),
                ('twitter', models.CharField(blank=True, max_length=200)),
                ('whatsapp', models.CharField(blank=True, max_length=200)),
                ('facebook', models.CharField(blank=True, max_length=200)),
                ('instagram', models.CharField(blank=True, max_length=200)),
                ('recent_post', models.BooleanField(default=False)),
                ('recent_post_photo', models.ImageField(blank=True, upload_to='upload')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.category')),
                ('doctor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.doctor')),
            ],
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
                ('email', models.CharField(blank=True, max_length=200)),
                ('sent_at', models.CharField(blank=True, max_length=200)),
                ('cat', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.category')),
            ],
        ),
    ]
