import os

def all_trails(g):
    cursor = g.conn.cursor()
    cursor.execute("SELECT * FROM trails")
    trails = [dict(row) for row in cursor.fetchall()]
    return trails

#UI section 13
# Get trails associated with a user
def trails_by_user(g, username):
    cursor = g.conn.cursor()
    cursor.execute("select users.name,trail.name,dish.name,restaurant.name,menu.price,restaurant.location from users join trail on users.user_id=trail.user_id and users.name=? natural join menu join dish on menu.dish_id=dish.dish_id join restaurant on menu.restaurant_id=restaurant.restaurant_id", (username))
    trails=[dict(row) for row in cursor.fetchall()]
    return trails

#UI section 11
# Filter by name of a trail and provide details of the item and restaurant
def trails_by_name(g, name):
    cursor=g.conn.cursor()
    cursor.execute("select restaurant.name, location, dish.name, menu.price, restaurant.cuisine_type, dish.dietary_tags from trail natural join menu join dish on dish.dish_id=menu.dish_id join restaurant on restaurant.restaurant_id=menu.restaurant_id where trail.name=?", (name))
    trails=[dict(row) for row in cursor.fetchall()]
    return trails



