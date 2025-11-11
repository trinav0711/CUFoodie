import os

# Base SQL to get dishes joined with restaurant and menu
def get_join_restaurant_dish_menu():
    return (
        "SELECT dish.dish_id, restaurant.restaurant_id, restaurant.name AS restaurant_name, "
        "location, dish.name AS dish_name, price, dietary_tags "
        "FROM dish "
        "NATURAL JOIN menu "
        "JOIN restaurant ON menu.restaurant_id = restaurant.restaurant_id"
    )

# Get dishes filtered by name
def get_dish_by_name(g, name):
    cursor = g.conn.cursor()
    query = get_join_restaurant_dish_menu() + " WHERE dish.name ILIKE %s"
    cursor.execute(query, (f"%{name}%",))
    cols = [desc[0] for desc in cursor.description]
    rows = [dict(zip(cols, row)) for row in cursor.fetchall()]
    cursor.close()
    return rows

# Get dishes filtered by maximum price
def get_dish_by_price(g, price):
    cursor = g.conn.cursor()
    query = get_join_restaurant_dish_menu() + " WHERE menu.price <= %s"
    cursor.execute(query, (price,))
    cols = [desc[0] for desc in cursor.description]
    rows = [dict(zip(cols, row)) for row in cursor.fetchall()]
    cursor.close()
    return rows

# Get dishes filtered by dietary tag
def get_dish_by_tag(g, tag):
    cursor = g.conn.cursor()
    query = get_join_restaurant_dish_menu() + " WHERE dish.dietary_tags ILIKE %s"
    cursor.execute(query, (f"%{tag}%",))
    cols = [desc[0] for desc in cursor.description]
    rows = [dict(zip(cols, row)) for row in cursor.fetchall()]
    cursor.close()
    return rows

