# Generated by Django 2.0.4 on 2018-04-09 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fractals', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuration',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
