import os

def get_restaurant_by_name(g, name):
    cursor = g.conn.cursor()
    cursor.execute("SELECT name FROM restaurant WHERE name=?", (name))
    rows=cursor.fetchall()
    return [dict(row) for row in rows] if rows else []
