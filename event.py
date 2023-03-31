from datetime import datetime
from flask import abort, make_response
from conection import engine
from sqlalchemy import text


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
    return EVENT


def create(event):
    EVENT = load_events_from_db()
    event_id = event.get("event_id")
    event_title = event.get("event_title", "")
    event_description = event.get("event_description", "")
    event_date = event.get("event_date", "")
    user_id = event.get("user_id")

    if event_id and event_id not in EVENT:
        sql = "INSERT INTO shedule_event (event_title, event_description, event_date, user_id) VALUES (%s, %s, %s, %s)"
        values = (event_title, event_description, event_date, user_id)
        with engine.connect() as conn:
            events = conn.execute(sql,values)
            conn.commit()
            return make_response(
            f"{events[event_title]} successfully created", 200
        )
    else:
        abort(
            406,
            f"User with last name {user_id} already exists",
        )


def read_one(event_id):
    EVENT = load_events_from_db()
    if event_id in EVENT:
        with engine.connect() as conn:
            event = conn.execute('SELECT * FROM schedule_event WHERE event_id = %i', event_id)
            conn.commit()
        return event[event_id]
    else:
        abort(
            404, f"Event with ID {event_id} not found"
        )


def update(event_id, event):
    if event_id in event:
        event_title_up = event.get("event_title", "")
        event_description_up = event.get("event_description", "")
        event_date_up = event.get("event_date", "")
        event_status_up = event.get("event_status", "")
        user_id = event.get("user_id", "")
        sql = "UPDATE shedule_event SET event_title = %s, event_description = %s, event_date = %s, event_status = %i WHERE event_id = %i;"
        values = (event_title_up, event_description_up, event_date_up, event_status_up, user_id)

        with engine.connect() as conn:
            result = conn.execute(sql, values)
            conn.commit()
        return result[user_id]
    else:
        abort(
            404,
            f"Event with ID {event_id} not found"
        )


def delete(event_id):
    event = load_events_from_db()
    if event_id in event:
        with engine.connect() as conn:
            event = conn.execute('DELETE FROM shedule_event WHERE event_id = {id}'.format(id=event_id))
            conn.commit()
            return make_response(
                f"{event_id} successfully deleted", 200
            )
    else:
        abort(
            404,
            f"Person with ID {event_id} not found"
        )