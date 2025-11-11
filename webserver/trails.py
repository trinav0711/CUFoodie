import os

#def all_trails(g):
#    cursor = g.conn.cursor()
#    cursor.execute("SELECT * FROM trails")
#    rows=cursor.fetchall()
#    return [dict(row) for row in rows] if rows else []
#
##UI section 13
## Get trails associated with a user
#def trails_by_user(g, username):
#    cursor = g.conn.cursor()
#    cursor.execute("select users.name,trail.name,dish.name,restaurant.name,menu.price,restaurant.location from users join trail on users.user_id=trail.user_id and users.name=? natural join menu join dish on menu.dish_id=dish.dish_id join restaurant on menu.restaurant_id=restaurant.restaurant_id", (username,))
#    rows=cursor.fetchall()
#    return [dict(row) for row in rows] if rows else []
#
##UI section 11
## Filter by name of a trail and provide details of the item and restaurant
#def trails_by_name(g, name):
#    cursor=g.conn.cursor()
#    cursor.execute("select restaurant.name, location, dish.name, menu.price, restaurant.cuisine_type, dish.dietary_tags from trail natural join menu join dish on dish.dish_id=menu.dish_id join restaurant on restaurant.restaurant_id=menu.restaurant_id where trail.name=?", (name,))
#    rows=cursor.fetchall()
#    return [dict(row) for row in rows] if rows else []
#
#import os
#
# Helper: convert fetched rows to list of dictionaries
def rows_to_dicts(cursor):
    cols = [desc[0] for desc in cursor.description]
    return [dict(zip(cols, row)) for row in cursor.fetchall()]

# Get all trails
def all_trails(g):
    cursor = g.conn.cursor()
    query = "SELECT * FROM trail"
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

