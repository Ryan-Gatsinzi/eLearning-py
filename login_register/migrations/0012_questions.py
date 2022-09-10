# Generated by Django 4.0 on 2022-05-24 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_register', '0011_rename_teahcer_id_quiz_teacher_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='questions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_no', models.IntegerField()),
                ('question', models.CharField(max_length=255)),
                ('opt1', models.CharField(max_length=255)),
                ('opt2', models.CharField(max_length=255)),
                ('opt3', models.CharField(max_length=255)),
                ('opt4', models.CharField(max_length=255)),
                ('answer', models.CharField(max_length=255)),
                ('quiz_id', models.IntegerField()),
                ('teacher_id', models.IntegerField()),
                ('status', models.CharField(default='activated', max_length=255)),
            ],
        ),
    ]
