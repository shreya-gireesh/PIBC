# Generated by Django 5.1 on 2024-09-02 09:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0004_rename_admin_name_adminmodel_admin_first_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoanApplicationModel',
            fields=[
                ('form_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('district', models.CharField(max_length=100)),
                ('place', models.CharField(max_length=100)),
                ('loan_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('followup_date', models.DateField()),
                ('description', models.TextField()),
                ('executive_name', models.CharField(max_length=100)),
                ('mobileno_1', models.CharField(max_length=15)),
                ('mobileno_2', models.CharField(blank=True, max_length=15, null=True)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UserApp.adminmodel')),
                ('bank_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UserApp.bankmodel')),
                ('loan_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UserApp.loanmodel')),
                ('status_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UserApp.statusmodel')),
            ],
        ),
    ]
