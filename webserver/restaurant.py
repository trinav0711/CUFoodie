import os

# Helper: convert rows to list of dicts
def rows_to_dicts(cursor):
    cols = [desc[0] for desc in cursor.description]
    return [dict(zip(cols, row)) for row in cursor.fetchall()]

# Get restaurant by name
def get_restaurant_by_name(g, name):
    cursor = g.conn.cursor()
    query = "SELECT name, location, cuisine_type FROM restaurant WHERE name = %s"
    cursor.execute(query, (name,))
    rows = rows_to_dicts(cursor)
    cursor.close()
    return rows

# Get all restaurants
def get_all_restaurants(g):
    cursor = g.conn.cursor()
    query = "SELECT name, location, cuisine_type FROM restaurant"
    cursor.execute(query)
    rows = rows_to_dicts(cursor)
    cursor.close()
    return rows

# Get all dishes in the menu of a restaurant
def get_dishes_by_restaurant_name(g, name):
    cursor = g.conn.cursor()
    query = """
        SELECT dish.name AS dish_name, price, dietary_tags
        FROM menu
        NATURAL JOIN restaurant
        JOIN dish ON dish.dish_id = menu.dish_id
        WHERE restaurant.name = %s
    """
    cursor.execute(query, (name,))
    rows = rows_to_dicts(cursor)
    cursor.close()
    return rows

# Get average rating of a restaurant
def get_average_rating(g, name):
    cursor = g.conn.cursor()
    query = """
        SELECT restaurant.name, AVG(rating) AS average_rating
        FROM restaurant
        NATURAL JOIN review
        WHERE restaurant.name = %s
        GROUP BY restaurant.name
    """
    cursor.execute(query, (name,))
    row = cursor.fetchone()
    cursor.close()
    if not row:
        return []
    return [{"name": row[0], "average_rating": float(row[1]) if row[1] is not None else None}]

# Get restaurants by location
def get_by_location(g, loc):
    cursor = g.conn.cursor()
    query = "SELECT name, location, cuisine_type FROM restaurant WHERE location = %s"
    cursor.execute(query, (loc,))
    rows = rows_to_dicts(cursor)
    cursor.close()
    return rows

# Get restaurants by cuisine type
def get_by_cuisine(g, cuisine):
    cursor = g.conn.cursor()
    query = "SELECT name, location, cuisine_type FROM restaurant WHERE cuisine_type = %s"
    cursor.execute(query, (cuisine,))
    rows = rows_to_dicts(cursor)
    cursor.close()
    return rows

# Filter by at least an average rating
def at_least_rating(g, rating):
    cursor = g.conn.cursor()
    query = """
        SELECT name, location, cuisine_type, AVG(rating) AS avg_rating
        FROM restaurant
        NATURAL JOIN review
        GROUP BY name, location, cuisine_type
        HAVING AVG(rating) >= %s
    """
    cursor.execute(query, (rating,))
    rows = rows_to_dicts(cursor)
    cursor.close()
    return rows

# Apply all filters together
def all_filters(g, loc, cuisine, rating):
    cursor = g.conn.cursor()
    query = """
        SELECT name, location, cuisine_type, AVG(rating) AS avg_rating
        FROM restaurant
        NATURAL JOIN review
        WHERE location = %s AND cuisine_type = %s
        GROUP BY name, location, cuisine_type
        HAVING AVG(rating) >= %s
    """
    cursor.execute(query, (loc, cuisine, rating))
    rows = rows_to_dicts(cursor)
    cursor.close()
    return rows