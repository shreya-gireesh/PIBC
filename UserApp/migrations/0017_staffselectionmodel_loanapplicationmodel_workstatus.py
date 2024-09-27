# Generated by Django 5.1 on 2024-09-26 11:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0016_alter_loanapplicationmodel_assigned_to_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaffSelectionModel',
            fields=[
                ('selection_id', models.AutoField(primary_key=True, serialize=False)),
                ('selection', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='loanapplicationmodel',
            name='workstatus',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='UserApp.staffselectionmodel'),
        ),
    ]