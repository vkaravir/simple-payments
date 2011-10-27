from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    (r'^', include('paymentapi.urls')), # import urls from paymentapi app
    (r'^test/', 'paymentapi.views.test'),
    (r'^$', direct_to_template, {'template': 'payment/index.html'}),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)

from django.conf import settings
if settings.DEBUG:
  import os.path
  urlpatterns += patterns('',
     (r'^static/(?P<path>.*)$', 'django.views.static.serve',
               {'document_root': os.path.join(os.path.dirname(__file__), 'site-media').replace('\\','/'),
         'show_indexes': True}),
    )
