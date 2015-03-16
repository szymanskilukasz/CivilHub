# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialForumEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField(default='', verbose_name='content')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('date_changed', models.DateTimeField(auto_now=True, verbose_name='date edited')),
                ('creator', models.ForeignKey(related_name='social_entries', verbose_name='author', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
