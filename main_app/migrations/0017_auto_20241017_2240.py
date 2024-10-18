# Generated by Django 3.2.7 on 2024-10-18 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0016_alter_note_color'),
    ]

    operations = [
        migrations.CreateModel(
            name='VocabularyEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=100)),
                ('meaning', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='note',
            name='vocab',
        ),
        migrations.AddField(
            model_name='note',
            name='vocab_entries',
            field=models.ManyToManyField(blank=True, to='main_app.VocabularyEntry'),
        ),
    ]
