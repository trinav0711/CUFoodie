import os

# Helper: convert fetched rows to list of dictionaries
def rows_to_dicts(cursor):
    cols = [desc[0] for desc in cursor.description]
    return [dict(zip(cols, row)) for row in cursor.fetchall()]

# Get list and details of all users
def get_all_users(g):
    cursor = g.conn.cursor()
    query = "SELECT user_name, email, join_date FROM users"
    cursor.execute(query)
    rows = rows_to_dicts(cursor)
    cursor.close()
    return rows