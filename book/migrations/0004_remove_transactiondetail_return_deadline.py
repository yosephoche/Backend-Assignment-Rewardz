# Generated by Django 4.1.1 on 2022-09-10 08:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0003_transactiondetail_is_returned'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transactiondetail',
            name='return_deadline',
        ),
    ]
