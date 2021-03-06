# Generated by Django 3.2.9 on 2022-02-01 15:44

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_rappel'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='published',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='status',
            field=models.CharField(choices=[('draft', 'Brouillon'), ('edit', 'A publier')], default='draft', max_length=10),
        ),
        migrations.AlterField(
            model_name='rappel',
            name='content',
            field=tinymce.models.HTMLField(),
        ),
    ]
