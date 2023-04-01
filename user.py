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
    with engine.connect() as conn:
        sql = "select * from shedule_user"
        user = conn.execute(text(sql))
        user_list =  user.fetchall()
        user_dict = []
        for row in user_list:
            e_dict = {
                        'user_id': row[0],
                        'user_email': row[1],
                        'user_name': row[2],
                        'user_password': row[3],
                        'user_status': row[4]
                    }
            user_dict.append(e_dict)
        return user_dict

def create(user):
    user_id = user.get("user_id", "")
    user_email = user.get("user_email", "")
    user_name = user.get("user_name", "")
    user_password = user.get("user_password", "")
    user_status = user.get("user_status", "")

    sql = "insert into shedule_user (user_email, user_name, user_password, user_status) values ('{}', '{}', '{}', {})".format(user_email, user_name, user_password, user_status)
    with engine.connect() as conn:
        users = conn.execute(text(sql))
        if users:
            return True
        else:
            return False


def read_one(user_id):
    with engine.connect() as conn:
        sql = "select * from shedule_user where user_id = {}".format(user_id)
        user = conn.execute(text(sql))
        user_list = user.fetchone()
        if user:
            user_dict = {
                    'user_id': user_list[0],
                    'user_email': user_list[1],
                    'user_name': user_list[2],
                    'user_password': user_list[3],
                    'user_status': user_list[4]
            }

            return user_dict
        else:
            abort(
                404, f"Event with ID {user_id} not found"
            )


def update(user_id, user):
    USER = read_one(user_id)
    if USER:
        user_name_up = user.get("user_name", "")
        user_email_up = user.get("user_email", "")
        user_password_up = user.get("user_password", "")
        user_status_up = user.get("user_status", "")
        sql = "update shedule_user set user_name = '{}', user_email = '{}', user_password = '{}', user_status = {} where user_id = {};".format(user_name_up, user_email_up, user_password_up, user_status_up, user_id)
        with engine.connect() as conn:
            result = conn.execute(text(sql))
            return result.rowcount
    else:
        abort(
            404,
            f"Person with ID {user_id} not found"
        )


def delete(user_id):
    verificad = read_one(user_id)
    if verificad:
        sql = 'delete from shedule_user where user_id = {}'.format(user_id)
        with engine.connect() as conn:
            result = conn.execute(text(sql))
            if result:
                return True
            else:
                return False
    else:
        abort(
            404,
            f"Person with ID {user_id} not found"
        )


user = {
        "user_name": "adocica",
        "user_email": "Meu amor",
        "user_password": 0,
        "user_status": 1,
    }


print(delete(1))