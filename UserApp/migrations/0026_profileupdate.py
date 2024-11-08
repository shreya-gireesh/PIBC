# Generated by Django 5.1 on 2024-11-02 05:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0025_staffassignmentmodel_assigned_by_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileUpdate',
            fields=[
                ('update_id', models.AutoField(primary_key=True, serialize=False)),
                ('adhaar_no', models.CharField(blank=True, max_length=100, null=True)),
                ('adhaar_img', models.FileField(blank=True, null=True, upload_to='adhaar/')),
                ('pan_no', models.CharField(blank=True, max_length=100, null=True)),
                ('pan_img', models.FileField(blank=True, null=True, upload_to='pancard/')),
                ('cancelled_check', models.FileField(blank=True, null=True, upload_to='cancelled_check/')),
                ('bank_name', models.CharField(blank=True, max_length=100, null=True)),
                ('ifsc_code', models.CharField(blank=True, max_length=100, null=True)),
                ('account_no', models.CharField(blank=True, max_length=100, null=True)),
                ('branch', models.CharField(blank=True, max_length=100, null=True)),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UserApp.adminmodel')),
            ],
        ),
    ]
