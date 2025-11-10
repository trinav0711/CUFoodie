import os

# Helper: convert fetched rows to list of dictionaries
def rows_to_dicts(cursor):
    cols = [desc[0] for desc in cursor.description]
    return [dict(zip(cols, row)) for row in cursor.fetchall()]

# Get all reviews
def all_reviews(g):
    cursor = g.conn.cursor()
    query = "SELECT * FROM review"
    cursor.execute(query)
    reviews = rows_to_dicts(cursor)
    cursor.close()
    return reviews

# Get reviews associated with a specific user
def reviews_by_user(g, username):
    cursor = g.conn.cursor()
    query = """
        SELECT user_name, name AS restaurant_name, location, cuisine_type,
               rating, comment, review_date
        FROM review
        NATURAL JOIN restaurant
        WHERE user_name = %s
    """
    cursor.execute(query, (username,))
    rows = rows_to_dicts(cursor)
    cursor.close()
    return rows

# Count how many reviews a user has written
def count_review_by_user(g, username):
    return len(reviews_by_user(g, username))