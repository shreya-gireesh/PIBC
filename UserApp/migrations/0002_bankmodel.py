# Generated by Django 5.1 on 2024-09-02 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankModel',
            fields=[
                ('bank_id', models.AutoField(primary_key=True, serialize=False)),
                ('bank_name', models.CharField(max_length=100)),
            ],
        ),
    ]
