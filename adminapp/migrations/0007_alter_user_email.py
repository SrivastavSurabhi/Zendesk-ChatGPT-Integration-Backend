# Generated by Django 3.2.18 on 2023-06-22 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0006_alter_user_zendeskorganizationid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=50),
        ),
    ]