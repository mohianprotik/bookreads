# Generated by Django 3.1.7 on 2021-03-15 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review_system', '0003_auto_20210316_0113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='tags',
            field=models.ManyToManyField(blank=True, to='review_system.Tag'),
        ),
    ]
