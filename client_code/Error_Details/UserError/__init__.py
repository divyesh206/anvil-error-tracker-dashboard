from ._anvil_designer import UserErrorTemplate
from .. import time_operations
from anvil import *
from m3._Components.Text import Text

class UserError(UserErrorTemplate):
    def __init__(self, **properties):

            
        self.init_components(**properties)
        
        if self.item['user']:
            self.email = self.item['user']['email']
        else:
            self.email = "Guest User"

        self.headline.text = f"{self.email} faced this issue"
        
        self.time.text = time_operations.get_relative_time(self.item['datetime'])
        for field, value in self.item['additional_info'].items():
            F=FlowPanel(gap="tiny",border="solid #3F484A 1px", spacing={"padding": 10, "margin" : 0})
            F.add_component(Text(text=field.capitalize(), bold= True, text_color="theme:On Surface Variant"))
            F.add_component(Text(text=value, bold= False), expand= True)
            self.additional_details_panel.add_component(F)
        self.session_link.url = f"https://anvil.works/build/apps/BVKJHWRTBSCSLR4L/sessions/{self.item['additional_info']['session']}"

    def additional_details_toggle_click(self, **event_args):
        
        self.additional_details_panel.visible = not self.additional_details_panel.visible
        self.additional_details_toggle.icon="mi:keyboard_arrow_down" if self.additional_details_panel.visible else "mi:keyboard_arrow_right"