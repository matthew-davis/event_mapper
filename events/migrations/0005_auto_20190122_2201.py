# Generated by Django 2.1.5 on 2019-01-22 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_auto_20190122_0609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='DateAdded',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
