# Generated by Django 3.0.4 on 2020-06-17 13:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('minimum_fund', models.PositiveIntegerField(verbose_name='Minimum fund')),
                ('maximum_fund', models.PositiveIntegerField(verbose_name='Maximum fund')),
                ('validity_start_date', models.DateTimeField(verbose_name='Validity start date')),
                ('validity_end_date', models.DateTimeField(verbose_name='Validity end date')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coupons', to='organizations.Organization', verbose_name='Organization')),
            ],
        ),
    ]