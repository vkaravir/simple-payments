from django.conf import settings

def md5hex(tohash):
  """
  Calculates an MD5 checksum for the given string.
  """
  try:
    import hashlib # Python >=2.5
    m = hashlib.md5()
  except: # Python <2.5
    import md5
    m = md5.new()
  m.update(tohash)
  return m.hexdigest()

def get_secret_key(seller_id):
  """
  Calculates a secret token for the seller with the seller_id.
  """
  secret_str = "%s%s"%(seller_id, settings.SECRET_KEY)
  return md5hex(secret_str)
  
def check_md5(params):
  """
  Checks that the MD5 checksum of a payment matches the given checksum.
  """
  sid = params.get('sid', '')
  pid = params.get('pid', '')
  amount = params.get('amount', -1)
  token = get_secret_key(sid)
  checkstr = "pid=%s&sid=%s&amount=%s&token=%s"%(pid, sid, amount, token)
  return md5hex(checkstr) == params.get('checksum', '')