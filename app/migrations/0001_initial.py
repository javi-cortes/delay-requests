# Generated by Django 3.1.5 on 2021-01-26 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Requests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.TextField()),
                ('state', models.CharField(max_length=10)),
                ('datetime', models.DateTimeField(max_length=30)),
            ],
        ),
    ]