from ._anvil_designer import UserErrorTemplate
from .. import time_operations
from anvil import *
from m3._Components.Text import Text
from anvil.js import window
from ... import Globals

class UserError(UserErrorTemplate):
    def __init__(self, **properties):

            
        self.init_components(**properties)

        email = self.item['user_email'] or "Guest User"
        self.headline.text = f"{email} faced this issue"
        
        self.time.text = time_operations.get_relative_time(self.item['datetime'])
        for field, value in self.item['additional_info'].items():
            F=FlowPanel(gap="tiny",border="solid #3F484A 1px", spacing={"padding": 10, "margin" : 0})
            F.add_component(Text(text=field.capitalize(), bold= True, text_color="theme:On Surface Variant"))
            F.add_component(Text(text=value, bold= False), expand= True)
            self.additional_details_panel.add_component(F)
        
    def additional_details_toggle_click(self, **event_args):
        
        self.additional_details_panel.visible = not self.additional_details_panel.visible
        self.additional_details_toggle.icon="mi:keyboard_arrow_down" if self.additional_details_panel.visible else "mi:keyboard_arrow_right"

    def session_link_click(self, **event_args):
        app_id = Globals.app_id
        window.open(f"https://anvil.works/build/apps/{app_id}/sessions/{self.item['additional_info']['session']}", "_blank")
