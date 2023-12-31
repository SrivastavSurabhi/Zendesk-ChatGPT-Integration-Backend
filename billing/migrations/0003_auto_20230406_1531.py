# Generated by Django 3.2.18 on 2023-04-06 10:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0004_remove_user_zendeskorganization'),
        ('billing', '0002_alter_plan_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plan',
            old_name='productName',
            new_name='PlanKey',
        ),
        migrations.RenameField(
            model_name='plan',
            old_name='stripePlanKey',
            new_name='productKey',
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('subsId', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('stripeSubscriptionId', models.CharField(blank=True, max_length=200, null=True)),
                ('stripeStatus', models.CharField(blank=True, max_length=200, null=True)),
                ('customerId', models.CharField(blank=True, max_length=200, null=True)),
                ('productId', models.CharField(blank=True, max_length=200, null=True)),
                ('priceId', models.CharField(blank=True, max_length=200, null=True)),
                ('trialEndsAt', models.DateTimeField()),
                ('subscriptionEndsAt', models.DateTimeField()),
                ('invoiceId', models.CharField(blank=True, max_length=200, null=True)),
                ('invoiceDetail', models.CharField(blank=True, max_length=200, null=True)),
                ('createdOnUTC', models.DateTimeField(auto_now_add=True)),
                ('updatedOnUTC', models.DateTimeField(auto_now=True)),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminapp.user')),
            ],
        ),
    ]
