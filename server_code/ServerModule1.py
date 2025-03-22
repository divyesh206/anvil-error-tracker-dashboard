import anvil.server
from anvil.tables import app_tables
import anvil.tables.query as q
from datetime import datetime
import anvil.tables
import anvil.users
error_table_columns = q.fetch_only("error_msg", "user_count", "last_appeared", "status", "traceback", "first_appeared", "error_count")
timeline_columns = q.fetch_only("type", "datetime", "additional_info", user = q.fetch_only("email"), error = q.fetch_only(), admin_user = q.fetch_only("email"))

@anvil.server.callable(require_user=lambda user: user['enabled'])
def get_errors_init():
    user = anvil.users.get_user()
    last_opened = user['last_opened']
    app_data = app_tables.app_data.get()
    app_id = app_data['app_id'] if app_data else None
    active_errors = app_tables.error.search(q.fetch_only(), status=q.not_("fixed", "ignored"))
    if last_opened:
        new_errors = app_tables.error.search(q.fetch_only(), q.page_size(1), first_appeared=q.greater_than(last_opened))
    else:
        new_errors = []
    reappeared_errors = app_tables.error.search(q.fetch_only(),  q.page_size(1), error_table_columns, status="reappeared")
    user['last_opened'] = datetime.utcnow()
    return len(active_errors), len(new_errors), len(reappeared_errors), last_opened, app_id


@anvil.server.callable(require_user=lambda user: user['enabled'])
def get_app_id(app_id):
    return app_tables.app_data.get()['app_id']
    
@anvil.server.callable(require_user=lambda user: user['enabled'])
def set_app_id(app_id):
    app_tables.app_data.get()['app_id'] = app_id

@anvil.server.callable(require_user=lambda user: user['enabled'])
def get_error_timeline(error_row):
    return app_tables.timeline.search(error=error_row)

@anvil.server.callable(require_user=lambda user: user['enabled'])
def error_fix_toggle(error_row):
    error_row['status'] = "pending" if error_row['status'] == "fixed" else "fixed"
    if error_row['status'] == "fixed":
        app_tables.timeline.add_row(type="error_fixed",datetime=datetime.utcnow(), error=error_row, admin_user = anvil.users.get_user())

@anvil.server.callable(require_user=lambda user: user['enabled'])
def ignore_error_toggle(error_row):
    error_row['status'] = "ignored" if error_row['status'] != "ignored" else "pending"
    #app_tables.timeline.add_row(type="error_fixed",datetime=datetime.utcnow(), error=error_row)

@anvil.server.callable(require_user=lambda user: user['enabled'])
def get_errors(query, search_term, order_by):
    print(query)
    return app_tables.error.search(anvil.tables.order_by(order_by, ascending = False), 
                                   anvil.tables.order_by("last_appeared", ascending = False), 
                                   q.any_of(
                                       error_msg=q.ilike("%"+search_term+"%"), 
                                       users = [search_term]),
                                   **query)

@anvil.server.callable(require_user=lambda user: user['enabled'])
def clear_timeline(error_row):
    with anvil.tables.batch_delete:
        for row in app_tables.timeline.search(error = error_row):
            row.delete()
            
@anvil.server.callable(require_user=lambda user: user['enabled'])
def delete_error(error_row):
    clear_timeline(error_row)
    error_row.delete()

@anvil.server.callable(require_user=lambda user: user['enabled'])
def merge_error(error, merge_into_error):
    timeline = app_tables.timeline.search(q.fetch_only(), error=error)
    with anvil.tables.batch_update:
        for row in timeline:
            row['error'] = merge_into_error
        merge_into_error['error_count'] += error['error_count']
        users = merge_into_error['users']
        users.extend(error['users'])
        merge_into_error['users'] = list(set(users))
        merge_into_error['user_count'] = len(list(set(users)))
        sessions = merge_into_error['sessions']
        sessions.extend(error['sessions'])
        merge_into_error['sessions'] = list(set(sessions))
        merge_into_error['first_appeared'] = min(error['first_appeared'], merge_into_error['first_appeared'])
        merge_into_error['last_appeared'] = max(error['last_appeared'], merge_into_error['last_appeared'])

    error.delete()
        