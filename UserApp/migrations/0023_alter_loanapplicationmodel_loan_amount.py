# Generated by Django 5.1 on 2024-10-07 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0022_alter_loanapplicationmodel_district_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanapplicationmodel',
            name='loan_amount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
    ]