# Generated by Django 4.0.5 on 2022-06-18 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0003_alter_match_player_one_alter_match_player_two'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='score',
            field=models.CharField(max_length=10, null=True),
        ),
    ]