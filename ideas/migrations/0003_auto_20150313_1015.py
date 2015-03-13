# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0002_auto_20150313_0956'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vote',
            options={'verbose_name': 'vote', 'verbose_name_plural': 'votes'},
        ),
        migrations.AlterField(
            model_name='idea',
            name='description',
            field=models.TextField(default='', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='vote',
            name='user',
            field=models.ForeignKey(related_name='idea_votes', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set([('user', 'idea')]),
        ),
    ]
