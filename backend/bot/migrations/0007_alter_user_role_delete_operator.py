# Generated by Django 4.0 on 2024-01-13 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0006_operator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Admin'), (2, 'Operator'), (3, 'Xodim'), (4, 'Client')], null=True),
        ),
        migrations.DeleteModel(
            name='Operator',
        ),
    ]