# Generated by Django 3.0.4 on 2020-06-18 21:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='user',
            field=models.ForeignKey(default=13, on_delete=django.db.models.deletion.CASCADE, related_name='user_coupons', to=settings.AUTH_USER_MODEL, verbose_name='User'),
            preserve_default=False,
        ),
    ]
