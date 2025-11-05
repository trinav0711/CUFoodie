import os

# Get details of items and restaurants from menu based on a price filter
def get_details_by_price(g, price);
    cursor = g.conn.cursor()
    cursor.execute(" select restaurant.name, location, dish.name, price from menu natural join dish join restaurant on menu.restaurant_id=restaurant.restaurant_id where price<=?", (price))
    rows=cursor.fetchall()
    return [dict(row) for row in rows] if rows else []
