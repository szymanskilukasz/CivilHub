# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import projects.models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_socialproject_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialproject',
            name='image',
            field=models.ImageField(default='img/projects/default.jpg', upload_to=projects.models.get_upload_path),
            preserve_default=True,
        ),
    ]
