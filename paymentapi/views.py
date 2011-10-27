from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf
from django.template import RequestContext

from models import Payment
from forms import SecretKeyForm, PaymentForm
from utils import get_secret_key, check_md5, md5hex

def secret_key(request):
  """
  Allows users to generate a secret key for their seller id to use in communication
  with the payment API.
  """
  if request.method == 'GET':
    form = SecretKeyForm()
  else:
    form = SecretKeyForm(request.POST)
    if form.is_valid():
      sid = form.cleaned_data['sid']
      key = get_secret_key(sid)
      return render_to_response('payment/key_created.html', {'sid': sid, 'key': key}, 
                context_instance=RequestContext(request))

  context = {'form': form}
  context.update(csrf(request))
  return render_to_response('payment/key.html', context, 
            context_instance=RequestContext(request))
  
@csrf_exempt
def pay(request):
  """
  A view that handles a payment request. It checks the HTTP method and the payment
  checksum and in successful cases renders the payment "confirmation" page.
  """
  if request.method != 'POST': # only HTTP POSTs are allowed
    return HttpResponse("%s Not Allowed"%request.method, status=405)
  try:
    checksum_ok = check_md5(request.POST)
  except: # the md5 function can fail with non-ascii data
    checksum_ok = False
  if not checksum_ok:
    return HttpResponse("The checksum does not match the data", status=400)
  payment_form = PaymentForm(request.POST)
  if payment_form.is_valid():
    payment = payment_form.save()
    dev = True if 'dev' in request.POST else False
    return render_to_response('payment/pay.html', {'payment': payment, 'dev': dev}, 
              context_instance=RequestContext(request))
  else:
    return HttpResponse("Invalid or missing data POSTed", status=400)
  
def process_payment(request, ptype, payment_id):
  """
  Processes the payment after user confirmation. Parameter ptype can be one of success,
  cancel, and error. The user will be redirected to the correct URL depending on the ptype.
  """
  payment = get_object_or_404(Payment, pk=payment_id)
  url = getattr(payment, '%s_url'%ptype)
  if url.find("?") == -1:
    url += "?"
  checksum = md5hex("pid=%s&ref=%s&token=%s"%(payment.pid, payment.id, get_secret_key(payment.sid)))
  # pass the checksum along in the redirect for the seller
  url = "%s&pid=%s&ref=%s&checksum=%s"%(url, payment.pid, payment.id, checksum)
  return HttpResponseRedirect(url)
  
def test(request):
  """
  Allows for testing the service without actually calling it from code. Aids in testing in
  understanding the parameters as well as testing the success, error, and cancel urls.
  """
  payment = {'pid':'mytestsale','sid':'tester', 'amount':15, 'success_url': 'http://localhost:8000/success',
            'error_url': 'http://localhost:8000/error','cancel_url': 'http://localhost:8000/cancel'}
  token = get_secret_key(payment['sid'])
  checkstr = "pid=%s&sid=%s&amount=%s&token=%s"%(payment['pid'], payment['sid'], payment['amount'], token)
  from utils import md5hex
  payment['checksum'] = md5hex(checkstr)
  form = PaymentForm(payment)
  return render_to_response('payment/test.html', {'form': form}, 
            context_instance=RequestContext(request))