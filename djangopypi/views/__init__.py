from django.conf import settings
from django.http import HttpResponseNotAllowed

from djangopypi.decorators import csrf_exempt
from djangopypi.http import parse_distutils_request
from djangopypi.models import Package, Release
from djangopypi.views.xmlrpc import parse_xmlrpc_request

@csrf_exempt
def root(request, fallback_view=None, **kwargs):
    """ Root view of the package index, handle incoming actions from distutils
    or redirect to a more user friendly view """

    if request.method == 'POST':
        if request.META['CONTENT_TYPE'] == 'text/xml':
            return parse_xmlrpc_request(request)
        parse_distutils_request(request)
        action = request.POST.get(':action','')
    else:
        action = request.GET.get(':action','')
    
    if not action:
        if fallback_view is None:
            fallback_view = settings.DJANGOPYPI_FALLBACK_VIEW
        return fallback_view(request, **kwargs)
    
    if not action in settings.DJANGOPYPI_ACTION_VIEWS:
        print 'unknown action: %s' % (action,)
        return HttpResponseNotAllowed(settings.DJANGOPYPI_ACTION_VIEW.keys())
    
    return settings.DJANGOPYPI_ACTION_VIEWS[action](request, **kwargs)
