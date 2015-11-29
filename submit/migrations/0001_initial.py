# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='resume',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=100)),
                ('cover_letter', models.CharField(max_length=2000)),
                ('skills', models.CharField(max_length=3000)),
                ('experience', models.CharField(max_length=3000)),
                ('sub_date', models.DateField(verbose_name=b'Submit time')),
            ],
        ),
    ]
