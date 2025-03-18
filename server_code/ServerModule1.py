import anvil.server
from anvil.tables import app_tables
import anvil.tables.query as q
from datetime import datetime
import anvil.tables

error_table_columns = q.fetch_only("error_msg", "user_count", "last_appeared", "status", "traceback", "first_appeared", "error_count")
timeline_columns = q.fetch_only("type", "datetime", "additional_info", user = q.fetch_only("email"), error = q.fetch_only())

@anvil.server.callable(require_user=lambda user: user['enabled'])
def get_errors_init():

    order_by = [anvil.tables.order_by("user_count", ascending = False), anvil.tables.order_by("last_appeared", ascending = False)]
    
    user_data = app_tables.user_data.get()
    last_opened = user_data['last_opened']
    active_errors = app_tables.error.search(*order_by, error_table_columns, status=q.not_("fixed", "ignored"))
    if last_opened:
        new_errors = app_tables.error.search(*order_by, error_table_columns, first_appeared=q.greater_than(user_data["last_opened"]))
    else:
        new_errors = []
    reappeared_errors = app_tables.error.search(*order_by, error_table_columns, status="reappeared")
    user_data['last_opened'] = datetime.utcnow()
    return active_errors, new_errors, reappeared_errors, user_data['app_id'], last_opened

@anvil.server.callable(require_user=lambda user: user['enabled'])
def set_app_id(app_id):
    app_tables.user_data.get()['app_id'] = app_id

@anvil.server.callable(require_user=lambda user: user['enabled'])
def get_error_timeline(error_row):
    return app_tables.timeline.search(error=error_row)

@anvil.server.callable(require_user=lambda user: user['enabled'])
def error_fix_toggle(error_row):
    error_row['status'] = "pending" if error_row['status'] == "fixed" else "fixed"
    app_tables.timeline.add_row(type="error_fixed",datetime=datetime.utcnow(), error=error_row)

@anvil.server.callable(require_user=lambda user: user['enabled'])
def ignore_error_toggle(error_row):
    error_row['status'] = "ignored" if error_row['status'] != "ignored" else "pending"
    #app_tables.timeline.add_row(type="error_fixed",datetime=datetime.utcnow(), error=error_row)

@anvil.server.callable(require_user=lambda user: user['enabled'])
def get_errors(query, search_term, order_by):

    return app_tables.error.search(anvil.tables.order_by(order_by, ascending = False), anvil.tables.order_by("last_appeared", ascending = False), **query, error_msg=q.ilike("%"+search_term+"%"))

@anvil.server.callable
def clear_timeline(error_row):
    with anvil.tables.batch_delete:
        for row in app_tables.timeline.search(error = error_row):
            row.delete()
            
@anvil.server.callable
def delete_error(error_row):
    clear_timeline(error_row)
    error_row.delete()