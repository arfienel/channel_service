# Generated by Django 4.1 on 2022-08-17 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='cost_usd',
            field=models.IntegerField(),
        ),
    ]