# Generated by Django 3.2.11 on 2022-01-31 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0004_auto_20220131_1316'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='team_A_score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='match',
            name='team_B_score',
            field=models.IntegerField(default=0),
        ),
    ]
