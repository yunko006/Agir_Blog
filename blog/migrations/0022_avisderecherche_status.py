# Generated by Django 3.2.9 on 2022-06-19 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0021_avisderecherche_archiver'),
    ]

    operations = [
        migrations.AddField(
            model_name='avisderecherche',
            name='status',
            field=models.CharField(choices=[('intervenant', 'Intervenant'), ('porteur', 'Porteur Projet')], default='intervenant', max_length=20),
        ),
    ]
