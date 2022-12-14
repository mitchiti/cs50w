# Generated by Django 4.1.2 on 2022-11-12 07:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_listing_watching_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='description',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='listing',
            name='watching_users',
            field=models.ManyToManyField(blank=True, related_name='watchers', to=settings.AUTH_USER_MODEL),
        ),
    ]
