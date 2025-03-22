from anvil import *
from m3.components import TextBox
import anvil.server

app_id = None
last_opened = None
active_error = None

def get_app_id():
    global app_id
    if not app_id:
        
        Container = LinearPanel(spacing_below="none")
        APP_ID_Input = TextBox(label = "Enter App ID")
        Container.add_component(APP_ID_Input)
        Container.add_component(Label(text="Your APP ID will be used for generating dynamic Anvil Editor URLs", spacing_below="none"))
        alert(Container, title= "Set up your APP ID", dismissible= False, buttons=["Submit"])
        app_id = APP_ID_Input.text
        anvil.server.call("set_app_id", app_id)

    return app_id