from django import forms

from models import Payment

import re
sid_format = re.compile("^[a-zA-Z0-9]+$")

class SecretKeyForm(forms.Form):
  """
  Form used in the secret key generation.
  """
  sid = forms.RegexField(regex=sid_format, min_length=3, label='Seller id (sid)', 
                    error_messages={'invalid': 'The seller id should be an alphanumeric string.'})

class PaymentForm(forms.ModelForm):
  """
  Form for the Payment model.
  """
  checksum = forms.CharField()
  class Meta:
    model = Payment