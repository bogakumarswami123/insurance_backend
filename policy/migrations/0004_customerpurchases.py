# Generated by Django 3.1.1 on 2022-04-16 16:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('policy', '0003_policy'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerPurchases',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('policy_id', models.IntegerField()),
                ('customer_id', models.IntegerField()),
                ('purchased_date', models.DateField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]