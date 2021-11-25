import datetime

def get_current_time():
    now = datetime.datetime.now()
    return { 
            "year"  : now.year,
            "month" : now.month, 
            "day"   : now.day,
            "hour"  : now.hour,
            "minute": now.minute,
            "second": now.second
            }

print(get_current_time())