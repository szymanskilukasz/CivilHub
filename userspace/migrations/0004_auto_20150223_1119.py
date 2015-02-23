# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userspace', '0003_auto_20150217_1323'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='background_image',
            new_name='image',
        ),
    ]
