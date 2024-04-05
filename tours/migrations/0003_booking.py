# Generated by Django 4.1 on 2024-04-01 08:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('tours', '0002_remove_tour_availability_tour_availability_end_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='tours.tour')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='users.userprofile')),
            ],
        ),
    ]
