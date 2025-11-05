import os

def get_restaurant_by_name(g, name):
    cursor = g.conn.cursor()
    cursor.execute("SELECT name, location, cuisine_type FROM restaurant WHERE name=?", (name))
    rows=cursor.fetchall()
    return [dict(row) for row in rows] if rows else []

def get_all_restaurants(g):
    cursor = g.conn.cursor()
    cursor.execute("SELECT name, location, cuisine_type FROM restaurant")
    rows=cursor.fetchall()
    return [dict(row) for row in rows] if rows else []


# Get all dishes in the menu of a restaurant
def get_dishes_by_restaurant_name(g, name):
    cursor = g.conn.cursor()
    cursor.execute("SELECT dish.name, price, dietary_tags FROM menu NATURAL JOIN restaurant join dish on dish.dish_id=menu.dish_id where restaurant.name=?", (name))
    rows=cursor.fetchall()
    return [dict(row) for row in rows] if rows else []

# Get average rating of restaurant
def get_average_rating(g, name):
    cursor = g.conn.cursor()
    cursor.execute("SELECT avg(rating) FROM restaurant NATURAL JOIN review WHERE name=?", (name))
    rows=cursor.fetchone()
    return [dict(row) for row in rows] if rows else []

# Get by location
def get_by_location(g, loc):
    cursor = g.conn.cursor()
    cursor.execute("SELECT name, location, cuisine_type FROM restaurant WHERE location=?", (loc))
    rows=cursor.fetchall()
    return [dict(row) for row in rows] if rows else []

# Get by cuisine type like American
def get_by_cuisine(g, cuisine):
    cursor = g.conn.cursor()
    cursor.execute("SELECT name, location, cuisine_type FROM restaurant WHERE cuisine_type=?", (cuisine))
    rows=cursor.fetchall()
    return [dict(row) for row in rows] if rows else []

# Filter by at least an average rating
def at_least_rating(g, rating):
    cursor = g.conn.cursor()
    cursor.execute("SELECT name, location, cuisine_type, avg(rating) FROM restaurant NATURAL JOIN review GROUP BY 1,2,3 HAVING avg(rating)>=?", (rating))
    rows=cursor.fetchall()
    return [dict(row) for row in rows] if rows else []

# All the filters
def all_filters(g, loc, cuisine, rating):
    cursor = g.conn.cursor()
    cursor.execute("SELECT name, location, cuisine_type, avg(rating) FROM restaurant NATURAL JOIN review WHERE location=? AND cuisine_type=? GROUP BY 1,2,3 HAVING avg(rating)>=?", (loc,cuisine,rating))
    rows=cursor.fetchall()
    return [dict(row) for row in rows] if rows else []
