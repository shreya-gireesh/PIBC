# Generated by Django 5.1 on 2024-09-02 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0003_adminmodel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='adminmodel',
            old_name='admin_name',
            new_name='admin_first_name',
        ),
        migrations.AddField(
            model_name='adminmodel',
            name='admin_last_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='adminmodel',
            name='admin_id',
            field=models.CharField(max_length=20, primary_key=True, serialize=False, unique=True),
        ),
    ]
