# Generated by Django 2.0.4 on 2018-04-10 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fractals', '0002_auto_20180409_2300'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuration',
            name='computing',
            field=models.BooleanField(default=False),
        ),
    ]
