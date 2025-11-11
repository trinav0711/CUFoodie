# Helper: convert fetched rows to list of dictionaries
def rows_to_dicts(cursor):
    cols = [desc[0] for desc in cursor.description]
    return [dict(zip(cols, row)) for row in cursor.fetchall()]

def trails_by_id(g, trail_id):
    cursor = g.conn.cursor()
    query = """
        SELECT users.name AS user_name,
               trail.name AS trail_name,
               dish.name AS dish_name,
               restaurant.name AS restaurant_name,
               menu.price,
               restaurant.location
        FROM trail
        JOIN users ON users.user_id = trail.user_id
        JOIN menu ON menu.dish_id = trail.dish_id AND menu.restaurant_id = trail.restaurant_id
        JOIN dish ON dish.dish_id = menu.dish_id
        JOIN restaurant ON restaurant.restaurant_id = menu.restaurant_id
        WHERE trail.trail_id = %s
    """
    cursor.execute(query, (trail_id,))
    cols = [desc[0] for desc in cursor.description]
    rows = [dict(zip(cols, row)) for row in cursor.fetchall()]
    cursor.close()
    return rows

# Get all trails
def all_trails(g):
    cursor = g.conn.cursor()
    query = """
        SELECT 
            t.trail_id,
            t.name,
            u.name AS user_name,
            COUNT(t.dish_id) AS count_items
        FROM trail t
        JOIN users u ON t.user_id = u.user_id
        GROUP BY t.trail_id, t.name, u.name
        ORDER BY t.trail_id
    """
    cursor.execute(query)
    rows = rows_to_dicts(cursor)
    cursor.close()
    return rows

# UI section 13: Get trails associated with a specific user
def trails_by_user(g, username):
    cursor = g.conn.cursor()
    query = """
        SELECT users.name AS user_name,
               trail.name AS trail_name,
               dish.name AS dish_name,
               restaurant.name AS restaurant_name,
               menu.price,
               restaurant.location
        FROM users
        JOIN trail ON users.user_id = trail.user_id AND users.name = %s
        NATURAL JOIN menu
        JOIN dish ON menu.dish_id = dish.dish_id
        JOIN restaurant ON menu.restaurant_id = restaurant.restaurant_id
    """
    cursor.execute(query, (username,))
    rows = rows_to_dicts(cursor)
    cursor.close()
    return rows

# UI section 11: Filter by name of a trail and provide details of the item and restaurant
def trails_by_name(g, name):
    cursor = g.conn.cursor()
    query = """
        SELECT restaurant.name AS restaurant_name,
               restaurant.location,
               dish.name AS dish_name,
               menu.price,
               restaurant.cuisine_type,
               dish.dietary_tags
        FROM trail
        NATURAL JOIN menu
        JOIN dish ON dish.dish_id = menu.dish_id
        JOIN restaurant ON restaurant.restaurant_id = menu.restaurant_id
        WHERE trail.name = %s
    """
    cursor.execute(query, (name,))
    rows = rows_to_dicts(cursor)
    cursor.close()
    return rows

