# Generated by Django 3.2.9 on 2022-01-15 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20220115_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='rubrique',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='blog.rubrique'),
        ),
    ]
