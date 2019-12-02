# Generated by Django 2.2.3 on 2019-11-22 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newJob', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Species',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sp_class', models.CharField(default='---', max_length=100)),
                ('specie', models.CharField(default='---', max_length=100)),
                ('shortName', models.CharField(default='---', max_length=100)),
                ('db', models.CharField(default='---', max_length=100)),
                ('db_ver', models.CharField(default='---', max_length=100)),
                ('scientific', models.CharField(default='---', max_length=100)),
                ('taxID', models.CharField(default='---', max_length=100)),
                ('full', models.BooleanField(default=False)),
                ('hasTargetSequencesAndGO', models.BooleanField(default=False)),
            ],
        ),
    ]
