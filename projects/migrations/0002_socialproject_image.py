# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialproject',
            name='image',
            field=models.ImageField(default='img/projects/default.jpg', upload_to='img/projects/'),
            preserve_default=True,
        ),
    ]
