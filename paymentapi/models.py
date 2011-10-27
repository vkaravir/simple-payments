from django.db import models

class Payment(models.Model):
  """
  A simple model for a payment.
  """
  pid = models.CharField(max_length=255, 
        error_messages={'required': 'pid is required', 
                        'max_length': 'pid invalid length', 
                        'min_length': 'pid invalid length'})
  sid = models.CharField(max_length=255, 
        error_messages={'required': 'sid is required', 
                        'max_length': 'sid invalid length', 
                        'min_length': 'sid invalid length'})
  amount = models.DecimalField(max_digits=9, decimal_places=2, 
        error_messages={'required': 'amount is required', 
                        'invalid': 'amount not valid', 
                        'max_digits': 'amount not valid', 
                        'max_decimal_places': 'amount not valid'})
  success_url = models.URLField(verify_exists=False, 
        error_messages={'required': 'success_url is required', 
                        'invalid': 'success_url not valid URL'})
  cancel_url = models.URLField(verify_exists=False, 
        error_messages={'required': 'cancel_url is required', 
                        'invalid': 'cancel_url not valid URL'})
  error_url = models.URLField(verify_exists=False, 
        error_messages={'required': 'error_url is required', 
                        'invalid': 'error_url not valid URL'})