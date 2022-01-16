# Generated by Django 3.2.9 on 2022-01-03 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_blogpost_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='rubrique',
            name='category',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='blog.category'),
        ),
        migrations.AddField(
            model_name='rubrique',
            name='title',
            field=models.CharField(default='', max_length=50),
        ),
    ]
