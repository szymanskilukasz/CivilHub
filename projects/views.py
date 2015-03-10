# -*- coding: utf-8 -*-

# UWAGA: widoki, które są tutaj zdefiniowane, współpracują ściśle
# z aplikacją 'locations'. Ta aplikacja nie definiuje urli - korzystamy
# tutaj z lokalizacji. Widoki są zaprojektowane pod konkretny układ URL-i.

import json

from django.http import HttpResponse
from django.views.generic import View, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.contrib.auth.views import login_required
from django.contrib.contenttypes.models import ContentType

from locations.mixins import LocationContextMixin
from locations.models import Location
from userspace.models import UserProfile
from places_core.mixins import LoginRequiredMixin
from places_core.permissions import is_moderator

from .models import SocialProject, TaskGroup, Task
from .forms import CreateProjectForm, UpdateProjectForm, TaskGroupForm, TaskForm


@require_POST
@login_required
def set_element_order(request, content_type, object_id, direction):
    """ Ustawiamy porządek dla grup lub zadań. Do funkcji należy przekazać
    ID typu zawartości, ID obiektu oraz kierunek ('UP' lub 'DOWN'). """
    model = ContentType.objects.get(pk=content_type).model_class()
    obj = model.objects.get(pk=object_id)
    if direction == 'UP':
        obj.up()
    else:
        obj.down()
    if hasattr(obj, 'get_absolute_url'):
        redirect_url = obj.get_absolute_url()
    else:
        redirect_url = obj.project.get_absolute_url()
    return redirect(redirect_url)


@require_POST
@login_required
def toggle_task_state(request, pk):
    """ Zmieniamy stan zadania ukończony/nieukończony. """
    task = get_object_or_404(Task, pk=pk)
    if task.is_done:
        task.is_done = False
        message = _(u"Task marked as undone")
    else:
        task.is_done = True
        message = _(u"Task marked as finished")
    task.save()
    if request.is_ajax():
        context = json.dumps({
            'success': True,
            'is_done': task.is_done,
            'message': message,
        })
        return HttpResponse(context, content_type="application/json")
    return redirect(task.get_absolute_url())


class ProjectContextMixin(LocationContextMixin):
    """ Mixin dla formularzy do tworzenia zadań oraz grup zadań. """
    def get_context_data(self, form=None):
        group_id = self.kwargs.get('group_id')
        project_slug = self.kwargs.get('slug')
        location_slug = self.kwargs.get('location_slug')
        context = super(ProjectContextMixin, self).get_context_data(form)
        context['form'] = form
        if project_slug is not None:
            context['object'] = get_object_or_404(SocialProject, slug=project_slug)
        if location_slug is not None:
            context['location'] = get_object_or_404(Location, slug=location_slug)
        return context


class ProjectAccessMixin(LoginRequiredMixin, ProjectContextMixin):
    """
    Mixin dla widoków usuwania i edycji prjektów, zadań oraz grup zadań. Superużytkownik
    zawsze ma prawa dostępu do wszystkiego. Każdy może tworzyć nowe zadania i grupy,
    ale tylko twórcy, administratorzy oraz moderatorzy mogą je później edytować
    i usuwać. Oczywiście, niezalogowani userzy nie mogą nic.
    """
    @classmethod
    def check_access(cls, obj, user):
        # "Twórca" zawsze może usunąć swoje "dzieło"
        access = user.profile == obj.creator
        # Superadmin może wszystko
        if not access and request.user.is_superuser:
            access = True
        # Sprawdzamy prawa moderatora
        if not access:
            location = None
            if hasattr(obj, 'location'):
                location = obj.location
            elif hasattr(obj, 'project'):
                location = obj.project.location
            else:
                location = obj.group.project.location
            if is_moderator(request.user, location):
                access = True
        return access

    def get(self, request, location_slug=None, slug=None, group_id=None, task_id=None):
        obj = self.get_object()
        access = self.check_access(obj, request.user)
        if not access:
            raise PermissionDenied
        return super(ProjectAccessMixin, self).get(request)

    def post(self, request, slug=None, location_slug=None, group_id=None, task_id=None):
        obj = self.get_object()
        access = self.check_access(obj, request.user)
        if not access:
            raise PermissionDenied
        return super(ProjectAccessMixin, self).post(request)


class JoinProjectView(LoginRequiredMixin, LocationContextMixin, View):
    """ Dołączanie/odłączanie użytkownika od całego projektu. """
    def post(self, request, location_slug=None, slug=None):
        project = get_object_or_404(SocialProject, slug=slug)
        if request.user.profile in project.participants.all():
            project.participants.remove(request.user.profile)
            for group in project.taskgroup_set.all():
                for task in group.task_set.all():
                    if request.user.profile in task.participants.all():
                        task.participants.remove(request.user.profile)
            message = _("You are no longer in this project")
        else:
            project.participants.add(request.user.profile)
            message = _("You have joined to this project")
        if request.is_ajax():
            context = {'success': True, 'message': message,}
            return HttpResponse(context, content_type="application/json")
        return redirect(reverse('locations:project_details', kwargs={
            'location_slug': location_slug,
            'slug': project.slug,
        }))


class JoinTaskView(LoginRequiredMixin, LocationContextMixin, View):
    """ Dołączanie/odłączanie użytkowników od konkretnego zadania. """
    def post(self, request, location_slug=None, slug=None, task_id=None):
        task = get_object_or_404(Task, pk=task_id)
        if request.user.profile in task.participants.all():
            task.participants.remove(request.user.profile)
            message = _("You are no longer in this task")
        else:
            task.participants.add(request.user.profile)
            if not request.user.profile in task.group.project.participants.all():
                task.group.project.participants.add(request.user.profile)
            message = _("You have joined this task")
        if request.is_ajax():
            context = {'success': True, 'message': message,}
            return HttpResponse(context, content_type="application/json")
        return redirect(reverse('locations:task_details', kwargs={
            'location_slug': location_slug,
            'slug': task.group.project.slug,
            'task_id': task.pk,
        }))


class CreateTaskGroupView(ProjectContextMixin, CreateView):
    """ Tworzenie nowej grupy dla zadań. Widok przyjmuje tylko POST. """
    model = TaskGroup
    form_class = TaskGroupForm

    def get_success_url(self):
        return self.object.project.get_absolute_url()

    def get_initial(self):
        initial = super(CreateTaskGroupView, self).get_initial()
        project_slug = self.kwargs.get('slug')
        if project_slug is not None:
            initial.update({
                'project': get_object_or_404(SocialProject, slug=project_slug)
            })
        initial.update({'creator': self.request.user.pk})
        return initial


class UpdateTaskGroupView(ProjectAccessMixin, UpdateView):
    """ Edycja grupy dla zadań. """
    model = TaskGroup
    form_class = TaskGroupForm
    pk_url_kwarg = 'group_id'

    def get_success_url(self):
        return self.object.project.get_absolute_url()


class DeleteTaskGroupView(ProjectAccessMixin, DeleteView):
    """ Usuwamy grupy zadań. """
    model = TaskGroup
    pk_url_kwarg = 'group_id'

    def get_success_url(self):
        return self.object.project.get_absolute_url()


class CreateTaskView(ProjectContextMixin, CreateView):
    """ Tworzenie nowego zadania. """
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_initial(self):
        initial = super(CreateTaskView, self).get_initial()
        initial['creator'] = self.request.user.profile
        group_id = self.kwargs.get('group_id')
        if group_id is not None:
            initial['group'] = get_object_or_404(TaskGroup, pk=group_id)
        return initial


class UpdateTaskView(ProjectAccessMixin, UpdateView):
    """ Edycja istniejących zadań. """
    model = Task
    form_class = TaskForm
    pk_url_kwarg = 'task_id'


class DeleteTaskView(ProjectAccessMixin, DeleteView):
    """ Usuwamy zadania. """
    model = Task
    pk_url_kwarg = 'task_id'

    def get_success_url(self):
        return self.object.group.project.get_absolute_url()


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


class ProjectUpdateView(ProjectAccessMixin, UpdateView):
    """ Edycja istniejących projektów - tylko twórcy i moderatorzy. """
    model = SocialProject
    form_class = UpdateProjectForm
    template_name = 'projects/socialproject_update.html'


class ProjectSummaryView(LocationContextMixin, DetailView):
    """ Podsumowanie najważniejszych informacji o projekcie. """
    model = SocialProject
    template_name = 'projects/socialproject_summary.html'


class ProjectParticipantsView(LocationContextMixin, ListView):
    """ Lista uczetników prjektu. """
    model = UserProfile
    template_name = 'projects/socialproject_participants.html'
    paginate_by = 24
    project_slug = None

    def get_queryset(self):
        self.project_slug = self.kwargs.get('slug')
        project = get_object_or_404(SocialProject, slug=self.project_slug)
        return project.participants.all()

    def get_context_data(self):
        context = super(ProjectParticipantsView, self).get_context_data()
        context['object'] = get_object_or_404(SocialProject, slug=self.project_slug)
        return context


class ProjectDetailView(LocationContextMixin, DetailView):
    """ Strona podsumowania projektu. Tutaj sporo będzie się działo w JS. """
    model = SocialProject

    def get_context_data(self, object=None):
        context = super(ProjectDetailView, self).get_context_data()
        task_id = self.kwargs.get('task_id')
        if task_id is not None:
            context['active_task'] = get_object_or_404(Task, pk=task_id)
        else:
            try:
                context['active_task'] = self.get_object()\
                                        .taskgroup_set.first().task_set.first()
            except AttributeError:
                # Brak zadań w ramach tego projektu
                pass
        return context
