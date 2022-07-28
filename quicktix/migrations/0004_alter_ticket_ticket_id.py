# Generated by Django 4.0.6 on 2022-07-28 18:17

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('quicktix', '0003_ticket_ticket_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='ticket_id',
            field=models.UUIDField(default=uuid.UUID('d0e90f01-b399-4070-bee1-d29b6858aff3'), verbose_name='Ticket ID'),
        ),
    ]
