from ._anvil_designer import ErrorsDisplayerTemplate
import anvil.server
from .Error_Card import Error_Card
from .. import Globals
import anvil.tables.query as q

class ErrorsDisplayer(ErrorsDisplayerTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.for_merge = properties.get('for_merge')
        self.order_menu.selected_value = "Total Users"
        self.filter_menu.selected_value = "Active Errors"
        
    def refresh_errors(self, **event_args):
        self.filter_menu.items = {
                "Active Errors": {"status" : q.not_("fixed", "ignored")},
                "New Errors": {"first_appeared" : q.greater_than(Globals.last_opened)},
                "Reappeared Errors": {"status" : "reappeared"},
                "Fixed Errors": {"status" : "fixed"},
                "Ignored Errors": {"status" : "ignored"},
                "All Errors": {},
            }

        self.order_menu.items = {
            "Total Users" : "user_count",
            "Last Appeared" : "last_appeared",
            "Total Occurences" : "error_count"
        }

        
        
        self.results_panel.clear()
        for row in anvil.server.call('get_errors', self.filter_menu.items[self.filter_menu.selected_value], 
                                     self.search_input.text, 
                                     self.order_menu.items[self.order_menu.selected_value]):
            
            self.results_panel.add_component(Error_Card(item = row, for_merge = self.for_merge))

    def form_show(self, **event_args):
        self.refresh_errors()