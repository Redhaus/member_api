from flask import g
import psycopg2
from psycopg2.extras import DictCursor

URI = 'postgres://hdayvnowaommob:6772b3f0449d44efcbce9f940483e3d2e9a96cde4ef601fcbfc2d77639d18f9a@ec2-174-129-255-4.compute-1.amazonaws.com:5432/d97nph4o67hreo'


def connect_db():
    # provide uri connection path and dict cursor
    conn = psycopg2.connect(URI, cursor_factory=DictCursor)

    # autocommit after each action
    conn.autocommit = True

    # create cur to run queries on
    sql = conn.cursor()

    # return both connection and cursor
    return conn, sql


def get_db():
    # create connection
    db = connect_db()

    # check globals for connection and cursor if not add them
    if not hasattr(g, 'db_conn'):
        g.db_conn = db[0]
    if not hasattr(g, 'db_cur'):
        g.db_cur = db[1]

    return g.db_cur


def init_db():
    db = connect_db()

    db[1].execute(open('schema.sql', 'r').read())
    db[1].close()
    db[0].close()
