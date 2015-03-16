# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20150316_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialforumtopic',
            name='project',
            field=models.ForeignKey(related_name='discussions', default=1, verbose_name='project', to='projects.SocialProject'),
            preserve_default=False,
        ),
    ]
