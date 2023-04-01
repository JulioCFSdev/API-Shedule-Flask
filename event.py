from datetime import datetime
from flask import abort, make_response
from conection import engine
from sqlalchemy import text

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

def load_events_from_db():

    with engine.connect() as conn:
        result = conn.execute(text("select * from shedule_event"))
        column_names = result.keys()
        events = []
        for row in result.all():
            events.append(dict(zip(column_names, row)))
        return events

EVENT = load_events_from_db()

def read_all():
    with engine.connect() as conn:
        sql = "select * from shedule_event"
        event = conn.execute(text(sql))
        event_list =  event.fetchall()
        event_dict = []
        for row in event_list:
            e_dict = {
                        'event_id': row[0],
                        'event_title': row[1],
                        'event_description': row[2],
                        'event_date': row[3],
                        'event_status': row[4],
                        'user_id': row[5]
                    }
            event_dict.append(e_dict)
        return event_dict


def create(event):
    event_title = event.get("event_title", "")
    event_description = event.get("event_description", "")
    event_date = event.get("event_date", "")
    event_status = event.get("event_status", "")
    user_id = event.get("user_id")

    sql = "insert into shedule_event (event_title, event_description, event_date, event_status, user_id) values ('{}', '{}', '{}', {}, {})".format(event_title, event_description, event_date, event_status, user_id)
    with engine.connect() as conn:
        events = conn.execute(text(sql))
        return make_response(
        f"{events[event_title]} successfully created", 200
        )


def read_one(event_id):
    with engine.connect() as conn:
        sql = "select * from shedule_event where event_id = {}".format(event_id)
        event = conn.execute(text(sql))
        event_list = event.fetchone()
        if event:
            event_dict = {
                'event_id': event_list[0],
                'event_title': event_list[1],
                'event_description': event_list[2],
                'event_date': event_list[3],
                'event_status': event_list[4],
                'user_id': event_list[5]
            }

            return event_dict
        else:
            abort(
                404, f"Event with ID {event_id} not found"
            )


def update(event_id, event):
    verificad = read_one(event_id)
    if verificad:
        event_title_up = event.get("event_title", "")
        event_description_up = event.get("event_description", "")
        event_date_up = event.get("event_date", "")
        event_status_up = event.get("event_status", "")
        user_id = event.get("user_id", "")
        sql = "update shedule_event set event_title = '{}', event_description = '{}', event_date = '{}', event_status = {} where event_id = {};".format(event_title_up, event_description_up, event_date_up, event_status_up, user_id)
        with engine.connect() as conn:
            result = conn.execute(text(sql))
            return result.rowcount
    else:
        abort(
            404,
            f"Event with ID {event_id} not found"
        )


def delete(event_id):
    verificad = read_one(event_id)
    if verificad:
        sql = 'delete from shedule_event where event_id = {}'.format(event_id)
        with engine.connect() as conn:
            result = conn.execute(text(sql))
            if result:
                return True
            else:
                return False
    else:
        abort(404,f"Person with ID {event_id} not found")


event = {
        "event_title": "bbbb",
        "event_description": "bbbbbbbbbbbbbbbbbbbbbbbbbb",
        "event_status": 0,
        "user_id": 1,
        "event_date": get_timestamp(),
    }