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
        if name:
            rows = restaurant_mod.get_restaurant_by_name(g, name)
        elif location or cuisine or min_rating:
            rows = restaurant_mod.get_all_restaurants(g)  # fallback until filtering supported
        else:
            rows = restaurant_mod.get_all_restaurants(g)
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
@app.route("/api/dishes")
def api_dishes():
    name = request.args.get("name", "")
    tag = request.args.get("tag", "")
    max_price = request.args.get("price", "")

    # Fetch dishes with optional filters
    try:
        if name or tag or max_price:
            rows = menu_mod.filter_menu_items(g, name=name, tag=tag, max_price=max_price)
        else:
            # fallback: get everything from menu
            if hasattr(menu_mod, "get_all_menu"):
                rows = menu_mod.get_all_menu(g)
            else:
                rows = []
    except Exception as e:
        logger.exception("Error fetching dishes")
        return jsonify({"error": str(e)}), 500

    # Format output for frontend
    dishes = [
        {
            "dish_id": row.get("menu_id") or row.get("dish_id"),
            "name": row.get("name"),
            "restaurant_id": row.get("restaurant_id"),
            "restaurant_name": row.get("restaurant_name"),
            "price": row.get("price"),
            "dietary_tags": row.get("dietary_tags"),
        }
        for row in rows
    ]

    return jsonify(dishes)


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

