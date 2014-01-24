### A work in progress validation rules ###
### rules strings are included in the file because it's convenient :D ###
import re, socket, datetime

messages = {
    "required": "{} is required",
    "email": "{} must be a valid email",
    "min": "{} must be more than {} characters",
    "mind": "{} must be higher than {}",
    "max": "{} must be less than {} characters",
    "maxd": "{} must be lower than {}",
    "between": "{}'s length must be between {} and {} characters",
    "betweend": "{}'s value must be higher than {} and lower than {}",
    "ip4": "{} must be a valid ipv4 address",
    "ip6": "{} must be a valid ipv6 address",
    "numeric": "{} must be numerical",
    "integer": "{} must be an integer",
    "posinteger": "{} must be a positive integer",
    "url": "{} must be a valid url",
    "alpha": "{} must contain only alphabetical characters",
    "alpha_num": "{} must contain only alphabetical characters and/or numbers",
    "alpha_dash": "{} must contain only alphabetical characters or numbers",
    "date": "{} is not a valid date, the format must be {}",
}

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def required(value):
    return not len(str(value).strip()) == 0

def email(value):
    pattern = "^[a-z0-9]+([._-][a-z0-9]+)*@([a-z0-9]+([._-][a-z0-9]+))+$"
    return re.match(pattern, str(value).strip()) is not None


### min, validates if a string size is higher than the max constraint ###
### min, validates if a numerical value is higher than the min constraint ###
def min(value, constraint = None):

    if not constraint:
        raise ValueError('constraints are missing from the validation rule')

    if not is_number(constraint):
        raise ValueError('constraint is not a valid integer')

    constraint = float(constraint)
    
    if is_number(value):
        return float(value) >= constraint
    
    return len(value.strip()) >= constraint

### max, validates if a string size is lower than the max constraint ###
### max, validates if a numerical value is lower than the max constraint ###
def max(value, constraint = None):

    if not constraint:
        raise ValueError('constraints are missing from the validation rule')

    if not is_number(constraint):
        raise ValueError('constraint is not a valid integer')

    constraint = float(constraint)
    
    if is_number(value):
        return float(value) <= constraint
    
    return len(value.strip()) <= constraint

### between, validates if a string size is between 2 length ###
### between, validates if a numerical value is between 2 values ###
def between(value, constraint = None):

    if not constraint:
        raise ValueError('constraints are missing from the validation rule')

    try:
        constraints = constraint.split(',')
    except TypeError:
        raise TypeError('constraints are not a valid integer')

    if len(constraints) < 2:
        raise ValueError('constraints are missing from the validation rule')

    lower = float(constraints[0])
    higher = float(constraints[1])
    
    if is_number(value):
        return lower <= float(value) <= higher
    
    return lower <= len(value.strip()) <= higher

### ip4, validates if value is a real ipv4 address ###
def ip4(value):
    try:
        socket.inet_pton(socket.AF_INET, value)
    except AttributeError:
        try:
            socket.inet_aton(value)
        except socket.error:
            return False
        return value.count('.') == 3
    except socket.error:  # not a valid address
        return False

    return True

### ip6, validates if value is a real ipv6 address ###
def ip6(value):
    try:
        socket.inet_pton(socket.AF_INET6, value)
    except socket.error:
        return False
    return True

### url, validates if value is a real url ###
def url(value):
    """ Borrowed from Django ! Thanks to them """
    url_regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
        r'localhost|' # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return url_regex.match(value) is not None
    

### numeric, validates if value is numerical ###
def numeric(value):
    return is_number(value)

### alpha, validates if value contains only alphabetical characters ###
def alpha(value):
    return re.match('^[a-zA-Z]+$', value) is not None

### alpha_num, validates if value contains alphabetical characters and numbers ###
def alpha_num(value):
    return re.match('^[a-zA-Z0-9]+$', value) is not None

### alpha_dash, validates if value contains alphabetical characters, numbers and dashes ###
def alpha_dash(value):
    return re.match('^[a-zA-Z0-9][ A-Za-z0-9_-]*$', value) is not None

### integer, validates if value is an integer ###
def integer(value):
    try:
        int(value)
    except ValueError:
        return False

    return True

### posinteger, validates if value is a positive integer ###
def posinteger(value):
    try:
        int(value)
    except ValueError:
        return False

    return int(value) > 0

### date, validates a date against a format ###
def date(value, constraint):
    try:
        datetime.datetime.strptime(value, constraint)
    except ValueError:
        return False

    return True

