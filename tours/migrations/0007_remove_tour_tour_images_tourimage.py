# Generated by Django 5.0.4 on 2024-04-17 17:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0006_tour_tour_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tour',
            name='tour_images',
        ),
        migrations.CreateModel(
            name='TourImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='tour_images/')),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='tours.tour')),
            ],
        ),
    ]
