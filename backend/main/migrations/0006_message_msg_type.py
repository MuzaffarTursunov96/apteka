# Generated by Django 4.0 on 2024-01-15 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_telegramuser_firma_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='msg_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]