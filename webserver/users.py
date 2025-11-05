import os
# accessible as a variable in index.html:
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, abort

### We have a connection variable g whuch is connected to the database.

# Get list and details of all users
def get_all_users(g):
    cursor = g.conn.cursor()
    cursor.execute("SELECT name FROM users")
    rows=cursor.fetchall()
    return [dict(row) for row in rows] if rows else []
