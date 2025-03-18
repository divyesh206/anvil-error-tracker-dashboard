from ._anvil_designer import StatusChangeTemplate
from .. import time_operations
from anvil import *
from m3._Components.Text import Text
from m3._Components.Divider import Divider


class StatusChange(StatusChangeTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.time.text = time_operations.get_relative_time(self.item["datetime"])
        if self.item['type'] == "error_fixed":
            self.headline.text = "Error has been marked as fixed"
            self.icon.icon = "mi:check"
            self.icon.icon_color = "limegreen"
        elif self.item['type'] == "error_reappeared":
            self.headline.text = "Error has reappeared"
            self.icon.icon = "mi:warning"
            self.icon.icon_color = "theme:Error"