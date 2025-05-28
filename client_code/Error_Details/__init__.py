from ._anvil_designer import Error_DetailsTemplate
from .. import time_operations
from .StatusChange import StatusChange
from .UserError import UserError
import anvil.server
from anvil import get_open_form, confirm
from .. import Globals

class Error_Details(Error_DetailsTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)s
        Globals.active_error = self.item

    def format_traceback(self, traceback_list):
        formatted_lines = []
        for i, trace in enumerate(traceback_list):
            prefix = "at " if i == 0 else "called from "
            filename = '/'.join(trace['filename'].split('/')[1:]).replace(".py","").replace("/__init__","")
            line = f"{prefix} <u>{filename}</u> line {trace['lineno']}:{trace['colno']}<br>"
          
            formatted_lines.append(line)
        
        return " \n".join(formatted_lines)
        
    def timeline_panel_show(self, **event_args):
        
        self.timeline_panel.clear()
        
        with anvil.server.loading_indicator(self.timeline_panel, min_height=80):

            for row in anvil.server.call("get_error_timeline", self.item):
                if row['type'] == "user_error":
                    self.timeline_panel.add_component(UserError(item = row), index=0)
                elif row['type'] == "error_fixed":
                    self.timeline_panel.add_component(StatusChange(item = row), index=0)
                elif row['type'] == "error_reappeared":
                    self.timeline_panel.add_component(StatusChange(item = row), index=0)

    def fix_toggle_btn_click(self, **event_args):
        anvil.server.call("error_fix_toggle",self.item)
        self.refresh_data_bindings()
        self.timeline_panel_show()
        get_open_form().refresh()

    def form_refreshing_data_bindings(self, **event_args):
        status = self.item['status']
        if status == "fixed":
            self.status.foreground="limegreen"
        elif status == "ignored":
            self.status.foreground='theme:Outline'
        else:
           self.status.foreground='theme:Error'

        last_appeared = self.item['last_appeared']
        if last_appeared:
            self.recent.text = time_operations.get_relative_time(last_appeared)
        self.first_appeared.text = f"First Appeared on\n{time_operations.convert_to_local_time(self.item['first_appeared']).strftime('%d %B %Y, %-I:%M %p')}"

    def ignore_toggle_btn_click(self, **event_args):
        anvil.server.call("ignore_error_toggle",self.item)
        self.refresh_data_bindings()
        get_open_form().refresh()

    def clear_timeline_btn_click(self, **event_args):
        if confirm("Are you sure you wish to clear the timeline for this error? This action cannot be undone", title = "Clear Timeline?", buttons = ["Cancel", "Clear"]):
            anvil.server.call('clear_timeline', self.item)
            self.timeline_panel.clear()

    def delete_btn_click(self, **event_args):
        if confirm("You will lose all data and timeline for this error which cannot be recovered", title = "Delete Error?", buttons = ["Cancel", "Delete"]) == "Delete":
            anvil.server.call("delete_error", self.item)
            self.remove_from_parent()
            get_open_form().refresh()

    def form_show(self, **event_args):
        self.card_content_container_1.scroll_into_view()