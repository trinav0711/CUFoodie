import os

# Generic join used across functions here so need not repeat it
def get_join_restaurant_dish_menu():
    return "SELECT restaurant.name,location,dish.name,price,dietary_tags FROM dish NATURAL JOIN menu JOIN restaurant on menu.restaurant_id=restaurant.restaurant_id"

# Extract information by the name of a dish which might be served across several restauarants
def get_dish_by_name(g, name):
    cursor = g.conn.cursor()
    cursor.execute("? WHERE dish.name=?", (get_join_restaurant_dish_menu(),name))
    rows=cursor.fetchall()
    return [dict(row) for row in rows] if rows else []

# Get list at most a price
def get_dish_by_price(g, price):
    cursor=g.conn.cursor()
    cursor.execute("? WHERE price<=?", (get_join_restaurant_dish_menu(), price))
    rows=cursor.fetchall()
    return [dict(row) for row in rows] if rows else []

# Get by dietary tags
def get_dish_by_tag(g, tag):
    cursor=g.conn.cursor()
    cursor.execute("? WHERE dietary_tags LIKE ?", (get_join_restaurant_dish_menu(),f"%{tag}%"))
    rows=cursor.fetchall()
    return [dict(row) for row in rows] if rows else []
