# Generated by Django 3.1.7 on 2021-05-26 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_funded',
            field=models.BooleanField(default=False),
        ),
    ]
