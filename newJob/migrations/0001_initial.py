# Generated by Django 2.2.3 on 2019-11-22 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UploadFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255)),
                ('file', models.FileField(upload_to='temp/%Y%m%d%H%M')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]