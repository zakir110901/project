# Generated by Django 4.1.7 on 2023-02-27 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practice_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='pdf',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf', models.FileField(upload_to='uploads/')),
            ],
        ),
    ]