# Generated by Django 4.2.7 on 2024-10-01 10:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contestant',
            name='position',
        ),
        migrations.AddField(
            model_name='contestant',
            name='position',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vote.position'),
        ),
    ]