# Generated by Django 5.1 on 2024-09-12 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0013_alter_loanapplicationmodel_work_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminmodel',
            name='admin_last_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]