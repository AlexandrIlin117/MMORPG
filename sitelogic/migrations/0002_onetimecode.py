# Generated by Django 4.1.2 on 2022-10-25 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitelogic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OneTimeCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('one_username', models.CharField(max_length=150)),
                ('one_first_name', models.CharField(max_length=150)),
                ('one_last_name', models.CharField(max_length=150)),
                ('one_email', models.CharField(max_length=254)),
                ('one_data_in', models.DateTimeField(auto_now_add=True)),
                ('one_check_code', models.CharField(max_length=128)),
                ('one_password', models.CharField(default='GG', max_length=128)),
            ],
        ),
    ]
