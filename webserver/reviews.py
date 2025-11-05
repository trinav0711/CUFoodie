import os

def all_reviews(g):
    cursor = g.conn.cursor()
    cursor.execute("SELECT * FROM review")
    reviews = [dict(row) for row in cursor.fetchall()]
    return reviews

# Get reviews associated with a user
def reviews_by_user(g, username):
    cursor = g.conn.cursor()
    cursor.execute("select user_name,name,location,cuisine_type,rating,comment,review_date from review natural join restaurant where user_name=?", (username))
    rows=cursor.fetchall()
    return [dict(row) for row in rows] if rows else []

# Count of reviews by user. Use a previous function to get the length of the dict returned
def count_review_by_user(g, username):
    return len(reviews_by_user(g, username))
