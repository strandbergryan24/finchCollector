# Generated by Django 5.0.1 on 2024-03-11 18:11

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='feeding',
            options={'ordering': ['-date']},
        ),
        migrations.AddField(
            model_name='feeding',
            name='finch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.finch'),
            preserve_default=False,
        ),
    ]
