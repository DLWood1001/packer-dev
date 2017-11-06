# -*- mode: python -*-
# vi: set ft=python ts=2 sw=2 sts=2 et :

class MAC_Address(object):
  """Create an object that represents a MAC address.

  Parameters:
  mac_address -- A string representation of a MAC Address.
                 A integer representation of a MAC Address.
                 A MAC Address object (creates a copy).
  """
  def __init__(self, mac_address=None):
    self._mac_int = 0
    self._mac_mask = int('ffffffffffff', 16)

    if mac_address is not None:
      if type(mac_address) is int:
        self._mac_int = mac_address
      elif type(mac_address) is str:
        self._mac_int = self._to_int(mac_address)
      elif type(mac_address) is MAC_Address:
        self._mac_int = mac_address._mac_int

  def _to_int(self, mac_str):

    mac_hex = mac_str.replace(':', '')

    mac_int = int(mac_hex, 16)

    return mac_int

  def _to_str(self, mac_int):
    
    mac_hex = format(mac_int, '012x')

    mac_str = ':'.join(a+b for a,b in zip(mac_hex[::2], mac_hex[1::2]))

    return mac_str

  def _normalize_r_term(self, r_term):
    # Note (Dan): Handle the various object types for addition.
    # Note (Dan): r_term needs to be an integer, the IF tree guarantees that.
    if type(r_term) is int:
      pass
    elif type(r_term) is str:
      r_term = self._to_int(r_term)
    elif type(r_term) is MAC_Address:
      r_term = r_term._mac_int
    else:
      msg = 'unsupported operand type(s) for +: \'MAC_address\' and \'%s\'' \
        % type(r_term).__name__
      raise TypeError(msg)

    return r_term

  def __str__(self):
    return self._to_str(self._mac_int)

  def __int__(self):
    return self._mac_int

  def __hex__(self):
    return hex(self._mac_int)

  def __add__(self, r_term):

    l_term = self._mac_int

    r_term = self._normalize_r_term(r_term)

    result = l_term + r_term

    return MAC_Address(result)
  
  def __lt__(self, r_term):
    return (self._mac_int < r_term._mac_int)

  def __le__(self, r_term):
    return (self._mac_int <= r_term._mac_int)

  def __eq__(self, r_term):
    return (self._mac_int == r_term._mac_int)

  def __nq__(self, r_term):
    return (self._mac_int != r_term._mac_int)

  def __gt__(self, r_term):
    return (self._mac_int > r_term._mac_int)

  def __ge__(self, r_term):
    return (self._mac_int >= r_term._mac_int)

  def __and__(self, r_term):

    l_term = self._mac_int

    r_term = self._normalize_r_term(r_term)

    result = l_term & r_term

    return MAC_Address(result)

  def __or__(self, r_term):

    l_term = self._mac_int

    r_term = self._normalize_r_term(r_term)

    result = l_term | r_term

    return MAC_Address(result)

  def __xor__(self, r_term):

    l_term = self._mac_int

    r_term = self._normalize_r_term(r_term)

    result = l_term ^ r_term

    return MAC_Address(result)

  def __invert__(self):

    l_term = self._mac_int

    # Note (Dan): Because of python's two's complement, you must mask out the
    #             desired bits.
    result = ~l_term & self._mac_mask

    return MAC_Address(result)

  def __lshift__(self, r_term):

    l_term = self._mac_int

    r_term = self._normalize_r_term(r_term)

    result = l_term << r_term

    return MAC_Address(result)

  def __rshift__(self, r_term):

    l_term = self._mac_int

    r_term = self._normalize_r_term(r_term)

    result = l_term >> r_term

    return MAC_Address(result)

class MAC_Addresses(object):
  """Create an Iterator that represents a range of MAC addresses.

  Parameters:
  mac_start -- A string representation of a MAC Address.
               A integer representation of a MAC Address.
               A MAC Address object (creates a copy).
  mac_end   -- A string representation of a MAC Address.
               A integer representation of a MAC Address.
               A MAC Address object (creates a copy).
  step      -- A step interval for the Iterator. Default = 1.
  """
  def __init__(self, mac_start, mac_stop, step=1):
    self._mac_start = MAC_Address(mac_start)
    self._mac_stop = MAC_Address(mac_stop)
    self._step = step
    self._mac_current = None

  def __iter__(self):
    return self

  # Python3 Next Method Compatibility
  def __next__(self):
    return self.next()

  # Python2 Next Method Compatibility
  def next(self):
    if self._mac_current is None:
      self._mac_current = MAC_Address(self._mac_start)

    if self._mac_current >= self._mac_stop:
      raise StopIteration()

    current = MAC_Address(self._mac_current)

    self._mac_current = self._mac_current + self._step
      
    return current

  def reset(self):
    self._mac_current = None

    return True
