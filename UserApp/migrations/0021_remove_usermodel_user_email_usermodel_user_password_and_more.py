# Generated by Django 5.1 on 2024-10-02 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0020_alter_loanapplicationmodel_workstatus'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermodel',
            name='user_email',
        ),
        migrations.AddField(
            model_name='usermodel',
            name='user_password',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='user_last_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]