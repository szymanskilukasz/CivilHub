# -*- coding: utf-8 -*-
from django.views.generic import View, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from locations.mixins import LocationContextMixin
from places_core.mixins import LoginRequiredMixin
from places_core.permissions import is_moderator
from locations.models import Location

from .models import SocialProject
from .forms import CreateProjectForm, UpdateProjectForm


class JoinProjectView(LoginRequiredMixin, LocationContextMixin, View):
    """ Dołączanie/odłączanie użytkownika od całego projektu. """
    template = 'projects/socialproject_join.html'

    def post(self, request, location_slug=None, slug=None):
        if not request.user.is_authenticated:
            raise PermissionDenied
        project = get_object_or_404(SocialProject, slug=slug)
        if request.user.profile in project.participants.all():
            project.participants.remove(request.user.profile)
            message = _("You are no longer in this project")
        else:
            project.participants.add(request.user.profile)
            message = _("You have joined to this project")
        if request.is_ajax():
            context = {'success': True, 'message': message,}
            return HttpResponse(context, content_type="application/json")
        return redirect(reverse('locations:project_details', kwargs={
            'location_slug': location_slug,
            'slug': project.slug
        }))


class ProjectListView(LocationContextMixin, ListView):
    """ Lista projektów w ramach jednej lokalizacji. """
    model = SocialProject

    def get_queryset(self):
        location_slug = self.kwargs.get('location_slug')
        if location_slug is None:
            return SocialProject.objects.all()
        return SocialProject.objects.filter(location__slug=location_slug)


class CreateProjectView(LoginRequiredMixin, LocationContextMixin, CreateView):
    """ Tworzenie nowego projektu dla zalogowanych użytkowników. """
    model = SocialProject
    form_class = CreateProjectForm

    def get_context_data(self, form=None):
        context = super(CreateProjectView, self).get_context_data()
        context['form'] = form
        return context

    def get_initial(self):
        initial = super(CreateProjectView, self).get_initial()
        location_slug = self.kwargs.get('location_slug')
        if location_slug is not None:
            initial.update({
                'location': get_object_or_404(Location, slug=location_slug)
            })
        initial.update({'creator': self.request.user.pk})
        return initial


class ProjectUpdateView(LoginRequiredMixin, LocationContextMixin, UpdateView):
    """ Edycja istniejących projektów - tylko twórcy i moderatorzy. """
    model = SocialProject
    form_class = UpdateProjectForm
    template_name = 'projects/socialproject_update.html'

    def get(self, request, location_slug=None, slug=None):
        location_slug = self.kwargs.get('location_slug')
        if location_slug is not None:
            location = get_object_or_404(Location, slug=location_slug)
            if is_moderator(request.user, location):
                return super(ProjectUpdateView, self).get(request, location_slug, slug)
        raise PermissionDenied

    def get_context_data(self, form=None):
        context = super(ProjectUpdateView, self).get_context_data()
        context['form'] = form
        return context


class ProjectDetailView(LocationContextMixin, DetailView):
    """ Strona podsumowania projektu. Tutaj sporo będzie się działo w JS. """
    model = SocialProject
