import os
from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import logging
import psycopg2
from psycopg2 import pool
import traceback

# Import helper modules
import dish, menu as menu_mod, restaurant as restaurant_mod, reviews as reviews_mod, trails as trails_mod, users as users_mod

# --- Configuration ---
BASE_DIR = Path(__file__).resolve().parent
WEBROOT = BASE_DIR.parent
DEFAULT_DB_URI = (
    os.environ.get("DATABASEURI")
    or os.environ.get("DATABASE_URL")
    or "postgresql://tb3201:sriya@127.0.0.1:5432/proj1part2"
)

DB_MIN_CONN = int(os.environ.get("DB_MIN_CONN", 1))
DB_MAX_CONN = int(os.environ.get("DB_MAX_CONN", 100))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("server")

# --- Connection pool ---
try:
    connection_pool = psycopg2.pool.SimpleConnectionPool(DB_MIN_CONN, DB_MAX_CONN, DEFAULT_DB_URI)
    if connection_pool:
        logger.info("✅ Initialized psycopg2 connection pool (min=%d max=%d)", DB_MIN_CONN, DB_MAX_CONN)
except Exception:
    logger.exception("❌ Failed to initialize connection pool with DSN: %s", DEFAULT_DB_URI)
    connection_pool = None

# --- Helper g-like wrapper ---
class G:
    def __init__(self, conn):
        self.conn = conn

def with_conn(fn):
    """Decorator to provide DB connection as `g`."""
    def wrapper(*args, **kwargs):
        if connection_pool is None:
            return jsonify(error="DB pool not initialized"), 500
        conn = None
        try:
            conn = connection_pool.getconn()
            g = G(conn)
            result = fn(g, *args, **kwargs)
            return result
        except Exception as e:
            logger.exception("Error in DB operation: %s", e)
            return jsonify(error=str(e), traceback=traceback.format_exc()), 500
        finally:
            if conn:
                try:
                    connection_pool.putconn(conn)
                except Exception:
                    logger.exception("Failed to return connection to pool")
    wrapper.__name__ = fn.__name__
    return wrapper

# --- Flask app ---
app = Flask(__name__, static_folder=None)
CORS(app)

# --- Health check ---
@app.route("/api/health", methods=["GET"])
def health():
    ok = connection_pool is not None
    return jsonify(status="ok" if ok else "error", db_pool=bool(connection_pool))

# --- Users ---
@app.route("/api/users", methods=["GET"])
def api_get_users():
    @with_conn
    def _inner(g):
        rows = users_mod.get_all_users(g)
        return jsonify(rows)
    return _inner()

# --- Restaurants ---
@app.route("/api/restaurants", methods=["GET"])
def api_restaurants():
    name = request.args.get("name", "").strip()
    location = request.args.get("location", "").strip()
    cuisine = request.args.get("cuisine", "").strip()
    min_rating = request.args.get("minRating", "").strip()

    @with_conn
    def _inner(g):
        # 1️⃣ Search by exact restaurant name
        if name:
            rows = restaurant_mod.get_restaurant_by_name(g, name)

        # 2️⃣ Filtering
        elif location or cuisine or min_rating:
            rows = restaurant_mod.get_all_restaurants(g)

            # Filter by location (DB-level or Python)
            if location:
                rows = restaurant_mod.get_by_location(g, location)

            # Filter by cuisine (partial match)
            if cuisine:
                rows = [r for r in rows if cuisine.lower() in r["cuisine_type"].lower()]

            # Filter by min_rating
            if min_rating:
                rating_val = float(min_rating)
                filtered = []
                for r in rows:
                    avg = restaurant_mod.get_average_rating(g, r["name"])
                    avg_rating = avg[0]["average_rating"] if avg else 0
                    if avg_rating >= rating_val:
                        filtered.append(r)
                rows = filtered

        # 3️⃣ No filters → all restaurants
        else:
            rows = restaurant_mod.get_all_restaurants(g)

        # Add average rating for each restaurant
        for r in rows:
            avg = restaurant_mod.get_average_rating(g, r["name"])
            r["avg_rating"] = avg[0]["average_rating"] if avg else None

        return jsonify(rows)

    return _inner()

@app.route("/api/restaurants/<name>", methods=["GET"])
def api_restaurant_by_name(name):
    @with_conn
    def _inner(g, name):
        row = restaurant_mod.get_restaurant_by_name(g, name)
        if not row:
            return jsonify(error="not found"), 404
        return jsonify(row)
    return _inner(name)

# --- Dishes ---
from flask import request, jsonify
import dish as dish_mod

@app.route("/api/dishes", methods=["GET"])
def api_dishes():
    @with_conn
    def _inner(g):
        name = request.args.get("name", "").strip()
        tag = request.args.get("tag", "").strip()
        price = request.args.get("price", "").strip()

        # Build base query
        query = dish_mod.get_join_restaurant_dish_menu()
        conditions = []
        params = []

        if name:
            conditions.append("dish.name ILIKE %s")
            params.append(f"%{name}%")
        if tag:
            conditions.append("dietary_tags ILIKE %s")
            params.append(f"%{tag}%")
        if price:
            try:
                price_val = float(price)
                conditions.append("price <= %s")
                params.append(price_val)
            except ValueError:
                return jsonify({"error": "Invalid price"}), 400

        # Add WHERE clause if any condition exists
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        # Execute query
        cursor = g.conn.cursor()
        cursor.execute(query, tuple(params))
        cols = [desc[0] for desc in cursor.description]
        rows = [dict(zip(cols, row)) for row in cursor.fetchall()]
        cursor.close()

        # Format for React frontend
        formatted = [
            {
                "dish_id": r.get("dish_id"),
                "menu_id": r.get("menu_id"),
                "restaurant_id": r.get("restaurant_id"),
                "name": r.get("dish_name"),
                "restaurant_name": r.get("restaurant_name"),
                "price": float(r.get("price")) if r.get("price") is not None else None,
                "dietary_tags": r.get("dietary_tags") or "",
            }
            for r in rows
        ]

        return jsonify(formatted)

    return _inner()

# --- Menu / Budget ---
@app.route("/api/menu/price", methods=["GET"])
def api_menu_by_price():
    max_price = request.args.get("max_price", type=float)
    if max_price is None:
        return jsonify(error="max_price query param required"), 400
    @with_conn
    def _inner(g, max_price):
        rows = menu_mod.get_details_by_price(g, max_price)
        return jsonify(rows)
    return _inner(max_price)

@app.route("/api/budget", methods=["GET"])
def api_budget():
    max_price = request.args.get("max_price", type=float)
    if max_price is None:
        return jsonify(error="max_price query param required"), 400
    @with_conn
    def _inner(g, max_price):
        rows = menu_mod.get_details_by_price(g, max_price)
        return jsonify(rows)
    return _inner(max_price)

# --- Reviews ---
@app.route("/api/reviews", methods=["GET"])
def api_get_reviews():
    @with_conn
    def _inner(g):
        rows = reviews_mod.all_reviews(g)
        return jsonify(rows)
    return _inner()

# ✅ Added route for React's query-param style access:
@app.route("/api/reviews/user", methods=["GET"])
def api_reviews_user_query():
    username = request.args.get("user")
    if not username:
        return jsonify(error="username required"), 400
    @with_conn
    def _inner(g, username):
        rows = reviews_mod.reviews_by_user(g, username)
        return jsonify(rows)
    return _inner(username)

@app.route("/api/reviews/user/<username>", methods=["GET"])
def api_reviews_by_user(username):
    @with_conn
    def _inner(g, username):
        rows = reviews_mod.reviews_by_user(g, username)
        return jsonify(rows)
    return _inner(username)

@app.route("/api/reviews/count/<username>", methods=["GET"])
def api_count_reviews(username):
    @with_conn
    def _inner(g, username):
        c = reviews_mod.count_review_by_user(g, username)
        return jsonify(count=c)
    return _inner(username)

# --- Trails ---
@app.route("/api/trails", methods=["GET"])
def api_get_trails():
    @with_conn
    def _inner(g):
        rows = trails_mod.all_trails(g)
        return jsonify(rows)
    return _inner()

@app.route("/api/trails/user/<username>", methods=["GET"])
def api_trails_by_user(username):
    @with_conn
    def _inner(g, username):
        rows = trails_mod.trails_by_user(g, username)
        return jsonify(rows)
    return _inner(username)

@app.route("/api/trails/<int:trail_id>", methods=["GET"])
def api_trail_detail(trail_id):
    @with_conn
    def _inner(g, trail_id):
        cursor = g.conn.cursor()
        query = """
            SELECT t.trail_id, t.name AS trail_name, u.name AS user_name,
                   r.name AS restaurant_name, d.name AS dish_name, m.price, r.location
            FROM trail t
            JOIN users u ON t.user_id = u.user_id
            JOIN menu m ON t.dish_id = m.dish_id AND t.restaurant_id = m.restaurant_id
            JOIN dish d ON m.dish_id = d.dish_id
            JOIN restaurant r ON m.restaurant_id = r.restaurant_id
            WHERE t.trail_id = %s
        """
        cursor.execute(query, (trail_id,))
        rows = rows_to_dicts(cursor)
        cursor.close()
        return jsonify(rows)
    return _inner(trail_id)

def rows_to_dicts(cursor):
    cols = [desc[0] for desc in cursor.description]
    return [dict(zip(cols, row)) for row in cursor.fetchall()]

@app.route("/api/trails/name/<name>", methods=["GET"])
def api_trails_by_name(name):
    @with_conn
    def _inner(g, name):
        rows = trails_mod.trails_by_name(g, name)
        return jsonify(rows)
    return _inner(name)

# --- Profile ---
@app.route("/api/profile", methods=["GET"])
def api_profile():
    username = request.args.get("username")
    if not username:
        return jsonify(error="username required"), 400
    @with_conn
    def _inner(g, username):
        user_reviews = reviews_mod.reviews_by_user(g, username)
        user_trails = trails_mod.trails_by_user(g, username)
        return jsonify({"username": username, "reviews": user_reviews, "trails": user_trails})
    return _inner(username)

# --- Static Frontend Serving ---
def find_frontend_dist():
    candidates = [
        WEBROOT / "frontend" / "dist",
        WEBROOT / "frontend" / "build",
        WEBROOT / "frontend" / "dist" / "client"
    ]
    for c in candidates:
        if c.exists():
            return c
    return None

frontend_dist = find_frontend_dist()

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    if path.startswith("api"):
        return jsonify(error="Not found"), 404
    if frontend_dist:
        full = frontend_dist / path
        if path != "" and full.exists():
            return send_from_directory(str(frontend_dist), path)
        index = frontend_dist / "index.html"
        if index.exists():
            return send_from_directory(str(frontend_dist), "index.html")
    dev_index = WEBROOT / "frontend" / "index.html"
    if dev_index.exists():
        return send_from_directory(str(WEBROOT / "frontend"), "index.html")
    return jsonify(ok=True, msg="API running. Build the React frontend into frontend/dist to serve static files.")

# --- Main ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8111))
    logger.info("🚀 Starting server on port %d", port)
    app.run(host="0.0.0.0", port=port)

