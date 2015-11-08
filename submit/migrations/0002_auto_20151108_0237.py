# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RunningTotal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('current_top', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='resume',
            name='rank',
            field=models.CharField(default=b'', max_length=10),
        ),
        migrations.AddField(
            model_name='resume',
            name='score',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AddField(
            model_name='resume',
            name='sentiment_rank',
            field=models.CharField(default=b'', max_length=10),
        ),
        migrations.AlterField(
            model_name='resume',
            name='sub_date',
            field=models.DateTimeField(verbose_name=b'Submit time'),
        ),
    ]
