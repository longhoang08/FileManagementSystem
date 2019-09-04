import datetime
import os


def get_expired_time():
    return (datetime.datetime.now() +
            datetime.timedelta(minutes=int(os.environ['TOKEN_UPTIME'])))


# max age in seconds
def get_max_age():
    return int(os.environ['TOKEN_UPTIME']) * 60


def minutes_to_ms(minutes):
    return int(minutes) * 60000


def get_time_range_to_block():
    return int(os.environ['TIME_RANGE_TO_BLOCK']) * 60
