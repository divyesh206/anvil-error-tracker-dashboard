from ._anvil_designer import Error_CardTemplate
from anvil.js.window import Date, moment
import anvil.tz
from anvil import *
from ..Error_Details import Error_Details

class Error_Card(Error_CardTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        status = self.item['status']
        if status == "fixed":
            self.status.foreground="limegreen"
        elif status == "ignored":
            self.status.foreground='theme:Outline'
        else:
           self.status.foreground='theme:Error'

        last_appeared = self.item['last_appeared']
        if last_appeared:
            self.recent.text = self.get_relative_datetime(last_appeared.astimezone(anvil.tz.tzlocal()))

    
    def get_relative_datetime(self, notification_datetime,convert_to_local=True):
        js_date = Date(
            notification_datetime.year,
            notification_datetime.month - 1,
            notification_datetime.day,
            notification_datetime.hour,
            notification_datetime.minute,
            notification_datetime.second,
            notification_datetime.microsecond / 1000,
        )
        return moment(js_date).fromNow()

    def interactive_card_1_click(self, **event_args):
        get_open_form().layout.show_sidesheet = True
        get_open_form().sidesheet_content.clear()
        get_open_form().sidesheet_content.add_component(Error_Details(item = self.item))