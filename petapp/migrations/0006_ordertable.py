# Generated by Django 4.2.7 on 2024-01-08 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petapp', '0005_rename_toatlamt_cart_totalamt'),
    ]

    operations = [
        migrations.CreateModel(
            name='ordertable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=200)),
                ('lastname', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('contact', models.BigIntegerField()),
                ('city', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=200)),
                ('pincode', models.IntegerField()),
            ],
            options={
                'db_table': 'ordertable',
            },
        ),
    ]
