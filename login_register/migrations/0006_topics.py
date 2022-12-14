# Generated by Django 4.0 on 2022-05-23 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_register', '0005_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='topics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to='files/')),
                ('subject', models.IntegerField()),
                ('date_assigned', models.TimeField(max_length=255)),
                ('teacher', models.IntegerField()),
                ('status', models.CharField(max_length=255)),
            ],
        ),
    ]
