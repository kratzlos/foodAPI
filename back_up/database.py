from flask import g
import sqlite3

def connect_overviewDB():
    sql = sqlite3.connect('C:\\Users\\tobia\\Documents\\building\\foodAPI\\overview.db')
    sql.row_factory = sqlite3.Row
    return sql

def get_db_overview():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_overviewDB()
    return g.sqlite_db


def connect_db():
    sql = sqlite3.connect('C:\\Users\\tobia\\Documents\\building\\foodAPI\\foods.db')
    sql.row_factory = sqlite3.Row
    return sql


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db
