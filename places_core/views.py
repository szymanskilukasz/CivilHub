# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.cache import cache
from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.utils.translation import check_for_language
from django.utils.translation import ugettext as _
from django.views.generic import View
from django.views.generic.edit import CreateView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import get_current_site
from django.shortcuts import render
from .models import AbuseReport
from .forms import AbuseReportForm
# REST API
from urllib2 import unquote
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import permissions as rest_permissions
from .serializers import ContentTypeSerializer, PaginatedSearchSerializer


def flush_page_cache():
    """ Funkcja usuwa zapisane w cache szablony kiedy zmieniamy język witryny. """
    langs = [x[0] for x in settings.LANGUAGES]
    sections = ['home',]
    for l in langs:
        for s in sections:
            key = '_'.join([s, l])
            cache.delete(key)


@csrf_exempt
def token_check(request):
    """
    Sprawdzamy i logujemy tokeny uwierzytelniające z zewnętrznych serwisów.
    Trzeba pamiętać, żeby to potem usunąć!!!
    """
    import json, logging
    from django.utils import timezone

    logger = logging.getLogger('tokens')

    if request.method == 'POST':
        token = request.POST.get('token')
        logger.info(u"[{}]: {}".format(timezone.now(), token))
        return HttpResponse(json.dumps({'token': token}),
                            content_type="application/json")
    return render(request, 'places_core/fbtest.html', {})


class SearchResultsAPIViewSet(viewsets.ViewSet):
    """
    Wyszukiwarka dla aplikacji mobilnej. Umożliwia sprawdzenie wyników wyszukiwania
    przez podanie odpowiedniego hasła do wyszukania (oczywiście w formie url-friendly).
    Zwraca listę znalezionych obiektów zawierającą pola `name`, `content_type`
    oraz `object_pk`. System rozpoznaje frazy przepuszczone przez funkcje takie
    jak `encodeURI`, `encodeURIComponent` albo `urlencode`.
    
    #### Przykład zapytania:
    ```/api-core/search/?q=warszawa```
    """
    serializer_class = PaginatedSearchSerializer
    permission_classes = (rest_permissions.IsAuthenticatedOrReadOnly,)

    def _get_model_labels(self, ct_list):
        if not len(ct_list):
            return None
        return [ContentType.objects.get(pk=x).model_class() for x in ct_list]

    def get_queryset(self):
        from haystack.query import SearchQuerySet
        try:
            query_term = unquote(self.request.QUERY_PARAMS.get('q'))
            sqs = SearchQuerySet().filter(content=query_term)
            types = self.request.QUERY_PARAMS.get('ct', '').split(',')
            models = self._get_model_labels([int(x) for x in types if x])
            if models is not None:
                sqs = sqs.models(*models)
        except Exception:
            sqs = []
        return sqs

    def list(self, request):
        sqs = [x for x in self.get_queryset() if x.object is not None]
        paginator = Paginator(sqs, settings.LIST_PAGINATION_LIMIT)
        page = request.QUERY_PARAMS.get('page')
        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            results = paginator.page(1)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)
        serializer = self.serializer_class(results,
                                            context={'request': request})
        return Response(serializer.data)


class ContentTypeAPIViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Widok umożliwiający pobieranie ID typów zawartości na podstawie nazwy
    aplikacji lub modelu i vice-versa. Tylko zapytania GET! Domyślnie listowane
    są wszystkie typy zawartości.
    
    Wyszukiwać można na dwa sposoby, dodając parametry GET do zapytania:
        1. Podać ID konkretnego typu zawartości (np. ?id=8)
        2. Podać nazwę aplikacji i modelu (np. ?app_label=ideas&model=idea)
    """
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer
    paginate_by = None

    def get_queryset(self):
        app_label = self.request.QUERY_PARAMS.get('app_label', None)
        model = self.request.QUERY_PARAMS.get('model', None)
        id = self.request.QUERY_PARAMS.get('id', None)
        if id:
            return ContentType.objects.filter(pk=id)
        elif app_label and model:
            return ContentType.objects.filter(app_label=app_label, model=model)
        else:
            return ContentType.objects.all()


@csrf_exempt
def set_language(request):
    next = request.REQUEST.get('next', None)
    if not next:
        next = request.META.get('HTTP_REFERER', None)
    if not next:
        next = '/'
    response = HttpResponseRedirect(next)
    if request.method == 'POST':
        lang_code = request.POST.get('language', None)
        if lang_code and check_for_language(lang_code):
            flush_page_cache();
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME,
                                lang_code, 365*24*60*60, 
                                domain = settings.SESSION_COOKIE_DOMAIN)
    return response


class FileServeView(View):
    """ Widok serwujący pliki statyczne. """
    http_method_names = [u'get', u'head', u'options', u'trace']
    filename = None

    def get(self, request, filename=None):
        if filename: self.filename = filename
        try:
            f = open(self.filename)
            content = f.read()
            f.close()
        except IOError:
            return HttpResponseNotFound()
        return HttpResponse(content, content_type="text/plain")


class CreateAbuseReport(CreateView):
    """
    Static form to create abuse reports for different ContentTypes.
    """
    model = AbuseReport
    form_class = AbuseReportForm
    template_name = 'places_core/abuse-report.html'
    success_url = '/report/sent/'

    def get(self, request, *args, **kwargs):
        app_label = kwargs['app_label']
        model_label = kwargs['model_label']
        content_type = ContentType.objects.get_by_natural_key(app_label,
                                                              model_label)
        ctx = {
                'title': _('Send abuse report'),
                'form': AbuseReportForm(initial={
                    'content_type': content_type,
                    'object_pk': kwargs['object_pk'],
                }),
            }
        return render(request, self.template_name, ctx)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.sender = self.request.user
        obj.site = get_current_site(self.request)
        obj.save()
        return super(CreateAbuseReport, self).form_valid(form)

    def pre_save(self, obj):
        obj.sender = self.request.user
        obj.site = Site.objects.get_current().domain


def report_sent(request):
    ctx = {'title': _('Report sent')}
    return render(request, 'places_core/report-sent.html', ctx)
