import os

def get_join_restaurant_dish_menu():
    return (
        "SELECT restaurant.name AS restaurant_name, location, dish.name AS dish_name, "
        "price, dietary_tags "
        "FROM dish NATURAL JOIN menu "
        "JOIN restaurant ON menu.restaurant_id = restaurant.restaurant_id"
    )

def get_dish_by_name(g, name):
    cursor = g.conn.cursor()
    query = get_join_restaurant_dish_menu() + " WHERE dish.name = %s"
    cursor.execute(query, (name,))
    cols = [desc[0] for desc in cursor.description]
    rows = [dict(zip(cols, row)) for row in cursor.fetchall()]
    cursor.close()
    return rows

def get_dish_by_price(g, price):
    cursor = g.conn.cursor()
    query = get_join_restaurant_dish_menu() + " WHERE price <= %s"
    cursor.execute(query, (price,))
    cols = [desc[0] for desc in cursor.description]
    rows = [dict(zip(cols, row)) for row in cursor.fetchall()]
    cursor.close()
    return rows

def get_dish_by_tag(g, tag):
    cursor = g.conn.cursor()
    query = get_join_restaurant_dish_menu() + " WHERE dietary_tags ILIKE %s"
    cursor.execute(query, (f"%{tag}%",))
    cols = [desc[0] for desc in cursor.description]
    rows = [dict(zip(cols, row)) for row in cursor.fetchall()]
    cursor.close()
    return rows