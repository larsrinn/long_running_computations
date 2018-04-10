# Generated by Django 2.0.4 on 2018-04-10 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fractals', '0004_result'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='configuration',
            name='computing',
        ),
        migrations.RemoveField(
            model_name='configuration',
            name='image',
        ),
        migrations.AlterField(
            model_name='result',
            name='configuration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='fractals.Configuration'),
        ),
    ]