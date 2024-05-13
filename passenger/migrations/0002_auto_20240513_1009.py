# Generated by Django 3.2.17 on 2024-05-13 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passenger', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='emergencycontact',
            old_name='FirstName',
            new_name='FullName',
        ),
        migrations.RemoveField(
            model_name='emergencycontact',
            name='LastName',
        ),
        migrations.RemoveField(
            model_name='passenger',
            name='PassportCountry',
        ),
        migrations.RemoveField(
            model_name='passenger',
            name='PassportExpiration',
        ),
        migrations.RemoveField(
            model_name='passenger',
            name='PassportNumber',
        ),
        migrations.AddField(
            model_name='passenger',
            name='Gender',
            field=models.CharField(default='Other', max_length=100),
        ),
        migrations.AddField(
            model_name='passenger',
            name='Nationality',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='passenger',
            name='PhoneNumber',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
