# Generated by Django 4.1.7 on 2023-03-21 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rolesentimenttonemapping',
            name='user',
        ),
        migrations.AddField(
            model_name='rolesentimenttonemapping',
            name='isDefault',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='rolesentimenttonemapping',
            name='zendeskOrganizationId',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
