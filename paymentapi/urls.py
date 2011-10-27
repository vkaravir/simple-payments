from django.conf.urls.defaults import *

urlpatterns = patterns('paymentapi.views',
  (r'^key/$', 'secret_key'), # for generating the secret key
  (r'^pay/$', 'pay'), # for showing the payment confirmation
  (r'^(success|cancel|error)/(\d+)/$', 'process_payment'), # for processing the payment
)