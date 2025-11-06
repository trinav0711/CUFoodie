import os

# Get details of items and restaurants from menu based on a price filter
def get_details_by_price(g, price):
    cursor = g.conn.cursor()
    query = """
        SELECT 
            restaurant.name AS restaurant_name,
            restaurant.location,
            dish.name AS dish_name,
            menu.price
        FROM menu
        NATURAL JOIN dish
        JOIN restaurant ON menu.restaurant_id = restaurant.restaurant_id
        WHERE menu.price <= %s
    """
    cursor.execute(query, (price,))
    cols = [desc[0] for desc in cursor.description]
    rows = [dict(zip(cols, row)) for row in cursor.fetchall()]
    cursor.close()
    return rows