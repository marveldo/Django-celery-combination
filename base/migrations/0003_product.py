# Generated by Django 4.1.4 on 2023-10-27 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_myuser_is_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('product_price', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('product_about', models.TextField(blank=True, null=True)),
            ],
        ),
    ]