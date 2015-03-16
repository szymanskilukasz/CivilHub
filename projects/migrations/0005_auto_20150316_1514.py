# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_socialforumtopic_project'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='socialforumentry',
            options={'ordering': ['date_created'], 'verbose_name': 'forum entry', 'verbose_name_plural': 'forum entries'},
        ),
    ]
