# Generated by Django 3.1.14 on 2023-09-24 11:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0015_auto_20230924_1454'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pokemonentity',
            old_name='pokemon_type',
            new_name='pokemon',
        ),
    ]
