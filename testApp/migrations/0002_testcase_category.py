# Generated by Django 5.1.1 on 2024-11-16 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='testcase',
            name='category',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
