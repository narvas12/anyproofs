# Generated by Django 3.2.18 on 2023-05-02 18:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('automailer', '0003_rename_receiver_transaction_reciever'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='date',
            new_name='created_at',
        ),
    ]
