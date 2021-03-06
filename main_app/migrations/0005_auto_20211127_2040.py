# Generated by Django 3.2.7 on 2021-11-28 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_note_homescreen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='color',
            field=models.CharField(choices=[('#EAEC40', 'Dandelion'), ('#FF7EB9', 'pink'), ('#F275AD', 'Cyclamen'), ('#79CBC5', 'Pearl Aqua'), ('#FFFF97', 'Canary'), ('#7AFCFF', 'blue'), ('#FBAE4A', 'Pastel Orange'), ('#F3858E', 'Tulip'), ('#8D9440', 'Bright Green')], default='#F275AD', max_length=7),
        ),
        migrations.AlterField(
            model_name='note',
            name='notetype',
            field=models.CharField(choices=[('T', 'To-Do'), ('R', 'Reminder'), ('L', 'Vocab/Learning'), ('P', 'Photocard')], default='R', max_length=1),
        ),
    ]
