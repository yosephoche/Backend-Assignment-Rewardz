# Generated by Django 4.1.1 on 2022-09-10 12:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0005_remove_transaction_borrowed_at_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='qty',
            new_name='stock',
        ),
    ]
