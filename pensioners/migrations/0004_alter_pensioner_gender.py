# Generated by Django 5.1 on 2024-09-04 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pensioners', '0003_pensioner_phone_number_alter_pensioner_pension_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pensioner',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('None', 'None')], default='none', max_length=10),
        ),
    ]
