from sqlalchemy import create_engine
from sqlalchemy import text, engine

db_connection_string = "mysql+pymysql://1o2l26nwvbwiwk9s9cxu:pscale_pw_27GuyDocxpC8uq2IVYkbJc4iAnYdaVJAcf1qD11ohjy@aws.connect.psdb.cloud/shedule_project?charset=utf8mb4"

engine = create_engine(db_connection_string, connect_args={
    "ssl":{
        "ssl_ca": "/etc/ssl/cert.pem"
    }
})