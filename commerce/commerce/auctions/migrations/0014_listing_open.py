# Generated by Django 3.1.7 on 2021-05-03 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='open',
            field=models.BooleanField(default=False),
        ),
    ]
