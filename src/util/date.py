import datetime

def get_current_raw_time():
    """ Method to get raw just time info. """
    return datetime.time.now()

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