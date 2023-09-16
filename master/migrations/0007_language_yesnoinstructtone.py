# Generated by Django 3.2.18 on 2023-08-07 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0006_alter_rolesentimenttonemapping_zendeskorganizationid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('languageId', models.BigAutoField(primary_key=True, serialize=False)),
                ('replylanguageAPI', models.CharField(default='American English', max_length=500)),
                ('replylanguageUI', models.CharField(default='American English', max_length=500)),
                ('accountOwnerID', models.CharField(default=1, max_length=50)),
                ('createdBy', models.IntegerField(blank=True, null=True)),
                ('createdOnUtc', models.DateTimeField(auto_now_add=True)),
                ('modifiedBy', models.IntegerField(blank=True, null=True)),
                ('modifiedOnUtc', models.DateTimeField(auto_now=True)),
                ('isDeleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='YesNoInstructTone',
            fields=[
                ('yniId', models.BigAutoField(primary_key=True, serialize=False)),
                ('yniToneAPI', models.CharField(default='Polite', max_length=500)),
                ('yniToneUI', models.CharField(default='Polite', max_length=500)),
                ('accountOwnerID', models.CharField(default=1, max_length=50)),
                ('createdBy', models.IntegerField(blank=True, null=True)),
                ('createdOnUtc', models.DateTimeField(auto_now_add=True)),
                ('modifiedBy', models.IntegerField(blank=True, null=True)),
                ('modifiedOnUtc', models.DateTimeField(auto_now=True)),
                ('isDeleted', models.BooleanField(default=False)),
            ],
        ),
    ]