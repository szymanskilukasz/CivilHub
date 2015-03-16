# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_socialforumentry'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialforumentry',
            name='topic',
            field=models.ForeignKey(default=1, verbose_name='discussion', to='projects.SocialForumTopic'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='socialforumtopic',
            name='slug',
            field=models.CharField(default='', max_length=210, verbose_name='slug'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='socialforumtopic',
            name='description',
            field=models.TextField(default='', verbose_name='description', blank=True),
            preserve_default=True,
        ),
    ]
