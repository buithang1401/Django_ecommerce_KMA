# Generated by Django 2.2.13 on 2022-07-26 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clothes', '0011_auto_20220724_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(blank=True, choices=[('COD', 'COD'), ('Online_Banking', 'Online_Banking')], max_length=50, null=True),
        ),
    ]
