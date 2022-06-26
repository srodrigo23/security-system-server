import datetime

def get_current_raw_time():
    """ Method to get raw just time info. """
    return datetime.datetime.now()

def get_current_time():
    """ Method to return time dictionary. """
    now = datetime.datetime.now()
    return { 
        "year"  : now.year,
        "month" : now.month, 
        "day"   : now.day,
        "hour"  : now.hour,
        "minute": now.minute,
        "second": now.second
    }

def get_current_time_string():
    """ Current time string format. """
    now = get_current_time()
    return f"{now['year']}-{now['month']}-{now['day']} {now['hour']}:{now['minute']}:{now['second']}"

def get_date():
    now = get_current_time()
    return f"{now['day']}-{now['month']}-{now['year']}"

def get_time():
    now = get_current_time()
    return f"{now['hour']}:{now['minute']}:{now['second']}"