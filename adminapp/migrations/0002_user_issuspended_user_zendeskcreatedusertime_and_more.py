# Generated by Django 4.1.7 on 2023-03-20 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='isSuspended',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='zendeskCreatedUserTime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='zendeskOrganizationId',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='zendeskUserUrl',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='zendeskUserid',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]