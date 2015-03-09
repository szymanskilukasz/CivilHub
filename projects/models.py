# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from slugify import slugify

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from locations.models import Location, BackgroundModelMixin
from userspace.models import UserProfile


def get_upload_path(instance, filename):
    return 'img/projects/' + uuid4().hex + os.path.splitext(filename)[1]


@python_2_unicode_compatible
class SocialProject(BackgroundModelMixin, models.Model):
    """ """
    name = models.CharField(max_length=200, verbose_name=_(u"name"))
    slug = models.CharField(max_length=210, verbose_name=(u"slug"))
    description = models.TextField(blank=True, default='', verbose_name=_(u"description"))
    location = models.ForeignKey(Location, verbose_name=_(u"location"), related_name="projects")
    participants = models.ManyToManyField(UserProfile, verbose_name=_(u"participants"))
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_(u"date created"))
    date_changed = models.DateTimeField(auto_now=True, verbose_name=_(u"date changed"))
    is_done = models.BooleanField(default=False, verbose_name=_(u"finished"))
    creator = models.ForeignKey(UserProfile, verbose_name=_(u"created by"), related_name="projects")
    image = models.ImageField(blank=True, upload_to=get_upload_path, default='img/projects/default.jpg')

    class Meta:
        verbose_name = _(u"project")
        verbose_name_plural = _(u"projects")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('locations:project_details', kwargs={
            'location_slug': self.location.slug,
            'slug': self.slug
        })

    def save(self, *args, **kwargs):
        """
        Provides 'clean' slug for this object, adding number of such elements to base name.
        """
        slug = slugify(self.name)
        if not self.slug:
            self.slug = slug
        success = False
        retries = 0
        while not success:
            check = self.__class__.objects.filter(slug=self.slug)\
                                          .exclude(pk=self.pk).count()
            if not check:
                success = True
            else:
                # We assume maximum number of 50 elements with the same name.
                # But the loop should be breaked if something went wrong.
                if retries >= 50:
                    raise ValidationError(u"Maximum number of retries exceeded")
                retries += 1
                self.slug = "{}-{}".format(slug, retries)
        super(SocialProject, self).save(*args, **kwargs)


@python_2_unicode_compatible
class TaskGroup(models.Model):
    """ """
    name = models.CharField(max_length=200, verbose_name=_(u"name"))
    description = models.TextField(blank=True, default='', verbose_name=_(u"description"))
    project = models.ForeignKey(SocialProject, verbose_name=_(u"project"))
    creator = models.ForeignKey(UserProfile, verbose_name=_(u"created by"), related_name="task_groups")

    class Meta:
        verbose_name = _(u"task group")
        verbose_name_plural = _(u"task groups")

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Task(models.Model):
    """ """
    name = models.CharField(max_length=200, verbose_name=_(u"name"))
    description = models.TextField(blank=True, default='', verbose_name=_(u"description"))
    group = models.ForeignKey(TaskGroup, verbose_name=_(u"group"))
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_(u"date created"))
    date_changed = models.DateTimeField(auto_now=True, verbose_name=_(u"date changed"))
    date_limited = models.DateTimeField(blank=True, null=True, verbose_name=_(u"time limit"))
    participants = models.ManyToManyField(UserProfile, verbose_name=_(u"participants"))
    is_done = models.BooleanField(default=False, verbose_name=_(u"finished"))
    creator = models.ForeignKey(UserProfile, verbose_name=_(u"created by"), related_name="tasks")

    class Meta:
        verbose_name = _(u"task")
        verbose_name_plural = _(u"tasks")

    def __str__(self):
        return self.name
