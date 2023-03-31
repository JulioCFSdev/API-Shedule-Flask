from datetime import datetime
from flask import abort, make_response
from conection import engine
from sqlalchemy import text


def load_users_from_db():

    with engine.connect() as conn:
        result = conn.execute(text("select * from shedule_user"))
        column_names = result.keys()
        users = []
        for row in result.all():
            users.append(dict(zip(column_names, row)))
        return users

USER = load_users_from_db()


def read_all():
    return USER


def create(user):
    user_name = user.get("user_name", "")
    user_email = user.get("user_email", "")
    user_password = user.get("user_password", "")
    user_status = user.get("user_status", "")
    sql = "INSERT INTO shedule_user (user_name, user_email, user_password, user_status) VALUES (%s, %s, %s, %s)"
    values = (user_name, user_email, user_password, user_status)

    with engine.connect() as conn:
        user = conn.execute(sql,values)
        conn.commit()
        return user


def read_one(user_id):
    USER = load_users_from_db()
    if user_id in USER:
        with engine.connect() as conn:
            user = conn.execute('SELECT * FROM schedule_user WHERE user_id = %i', user_id)
            conn.commit()
        return user[user_id]
    else:
        abort(
            404, f"Person with ID {user_id} not found"
        )


def update(user_id, user):
    USER = load_users_from_db()
    if user_id in USER:
        user_name_up = user.get("user_name", "")
        user_email_up = user.get("user_email", "")
        user_password_up = user.get("user_password", "")
        user_status_up = user.get("user_status", "")
        sql = "UPDATE shedule_user SET user_name = %s, user_email = %s, user_password = %s, user_status = %i WHERE user_id = %i;"
        values = (user_name_up, user_email_up, user_password_up, user_status_up, user_id)

        with engine.connect() as conn:
            result = conn.execute(sql, values)
            conn.commit()
        return result[user_id]
    else:
        abort(
            404,
            f"Person with ID {user_id} not found"
        )


def delete(user_id):
    USER = load_users_from_db()
    if user_id in USER:
        print(100)
        with engine.connect() as conn:
            user = conn.execute('DELETE FROM shedule_user WHERE user_id = {id}'.format(id=user_id))
            conn.commit()
        del user[user_id]
        return make_response(
            f"{user_id} successfully deleted", 200
        )
    else:
        abort(
            404,
            f"Person with ID {user_id} not found"
        )
