from anvil.js.window import Date, moment
import anvil.tz

def get_relative_time(datetime):
    datetime = convert_to_local_time(datetime)
    js_date = Date(
            datetime.year,
            datetime.month - 1,
            datetime.day,
            datetime.hour,
            datetime.minute,
            datetime.second,
            datetime.microsecond / 1000,
        )
    return moment(js_date).fromNow()

def convert_to_local_time(datetime):
    return datetime.astimezone(anvil.tz.tzlocal())