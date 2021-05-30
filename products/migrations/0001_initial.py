# Generated by Django 3.2 on 2021-05-29 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('sku', models.CharField(max_length=32, unique=True)),
                ('brand', models.CharField(max_length=16)),
                ('purchase_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('mrp', models.DecimalField(decimal_places=2, max_digits=10)),
                ('selling_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tax_code', models.IntegerField()),
                ('hsn', models.CharField(max_length=16)),
            ],
        ),
    ]