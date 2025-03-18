from ._anvil_designer import MainTemplate
import anvil.server
from ..Error_Card import Error_Card
from m3.components import TextBox
from anvil import alert, LinearPanel, Label
from .. import Globals
import anvil.tables.query as q
import anvil.tz
import anvil.users

class Main(MainTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        anvil.users.login_with_form(show_signup_option= True)
        self.order_menu.selected_value = "Total Users"
        print(anvil.app.environment)
        self.filter_menu.selected_value = "Active Errors"

        self.all_errors, self.new_errors, self.reappeared_errors, app_id, last_opened = anvil.server.call('get_errors_init')
        
        self.filter_menu.items = {
                "Active Errors": {"status" : q.not_("fixed", "ignored")},
                "New Errors": {"first_appeared" : q.greater_than(last_opened)},
                "Reappeared Errors": {"status" : "reappeared"},
                "Fixed Errors": {"status" : "fixed"},
                "Ignored Errors": {"status" : "ignored"},
                "Show All": {},
            }
        self.order_menu.items = {
            "Total Users" : "user_count",
            "Last Appeared" : "last_appeared",
            "Total Occurences" : "error_count"
        }
        
        if not app_id:
            Container = LinearPanel(spacing_below="none")
            APP_ID_Input = TextBox(label = "Enter App ID")
            Container.add_component(APP_ID_Input)
            Container.add_component(Label(text="Your APP ID will be used for generating correct URLs to Anvil Editor links", spacing_below="none"))
            alert(Container, title= "Set up your APP ID", dismissible= False, buttons=["Submit"])
            app_id = APP_ID_Input.text
            anvil.server.call("set_app_id", app_id)
            
        Globals.app_id = app_id
        Globals.last_opened = last_opened
        self.alL_errors_count.text = len(self.all_errors)
        self.new_errors_count.text = len(self.new_errors)
        self.reappeared_errors_count.text = len(self.reappeared_errors)
        self.layout.show_sidesheet = False
        
    def form_show(self, **event_args):
        for row in self.all_errors:
            self.results_panel.add_component(Error_Card(item = row))

    def icon_button_1_click(self, **event_args):
        self.layout.show_sidesheet = False
    

    def refresh_errors(self, **event_args):
        self.results_panel.clear()
        for row in anvil.server.call('get_errors', self.filter_menu.items[self.filter_menu.selected_value], 
                                     self.search_input.text, 
                                     self.order_menu.items[self.order_menu.selected_value]):
            
            self.results_panel.add_component(Error_Card(item = row))

