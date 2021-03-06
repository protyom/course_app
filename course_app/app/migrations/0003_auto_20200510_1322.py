# Generated by Django 3.0.5 on 2020-05-10 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_bankaccount_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankaccount',
            name='beta',
            field=models.CharField(blank=True, max_length=513, null=True),
        ),
        migrations.AddField(
            model_name='bankaccount',
            name='factor_1',
            field=models.CharField(blank=True, max_length=513, null=True),
        ),
        migrations.AddField(
            model_name='bankaccount',
            name='factor_2',
            field=models.CharField(blank=True, max_length=66, null=True),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='public_number',
            field=models.CharField(max_length=513),
        ),
    ]
