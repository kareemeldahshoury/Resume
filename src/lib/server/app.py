from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import sqlite3
import logging
import os
from threading import Lock
from mangum import Mangum

app = Flask(__name__, static_folder="static", static_url_path="/")
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Database configuration
DATABASE_PATH = 'visitors.db'
db_lock = Lock()

def init_database():
    """Initialize SQLite database and create table if it doesn't exist"""
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            # Create table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS visitor_stats (
                    id TEXT PRIMARY KEY,
                    count INTEGER DEFAULT 0
                )
            ''')
            
            # Insert initial visitor count if it doesn't exist
            cursor.execute('''
                INSERT OR IGNORE INTO visitor_stats (id, count) 
                VALUES (?, ?)
            ''', ('visitor_count', 0))
            
            conn.commit()
            logger.info("Database initialized successfully")
    except sqlite3.Error as e:
        logger.error(f"Database initialization error: {e}")
        raise

def get_visitor_count():
    """Get current visitor count from SQLite database"""
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT count FROM visitor_stats WHERE id = ?', ('visitor_count',))
            result = cursor.fetchone()
            return result[0] if result else 0
    except sqlite3.Error as e:
        logger.error(f"Error getting visitor count: {e}")
        return 0

def increment_visitor_count():
    """Increment visitor count in SQLite database"""
    with db_lock:  # Thread-safe increment
        try:
            with sqlite3.connect(DATABASE_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE visitor_stats 
                    SET count = count + 1 
                    WHERE id = ?
                ''', ('visitor_count',))
                
                # Get the updated count
                cursor.execute('SELECT count FROM visitor_stats WHERE id = ?', ('visitor_count',))
                result = cursor.fetchone()
                new_count = result[0] if result else 1
                
                conn.commit()
                logger.info(f"Visitor count incremented to: {new_count}")
                return new_count
        except sqlite3.Error as e:
            logger.error(f"Error incrementing visitor count: {e}")
            return get_visitor_count()  # Return current count on error

# Initialize database on startup
init_database()

@app.route("/api", methods=["GET"])
def visit():
    """Handle visitor count API endpoint"""
    logger.info(f"Request cookies: {dict(request.cookies)}")
    
    # Check if visitor has already been counted (cookie exists)
    if request.cookies.get("visited"):
        logger.info("Visitor has already been counted (cookie found)")
        current_count = get_visitor_count()
        return jsonify({"visits": current_count, "new_visitor": False})
    
    # New visitor - increment count
    logger.info("New visitor detected, incrementing count")
    try:
        new_count = increment_visitor_count()
        
        # Create response with updated count
        response = make_response(jsonify({
            "visits": new_count, 
            "new_visitor": True
        }))
        
        # Set cookie that expires in 1 hour (3600 seconds)
        response.set_cookie(
            "visited", 
            "true", 
            max_age=3600,  # 1 hour in seconds
            samesite='Lax',
            secure=True,  # Set to True if using HTTPS
            httponly=False  # Allow JavaScript access if needed
        )
        
        logger.info(f"New visitor count: {new_count}, cookie set")
        return response
        
    except Exception as e:
        logger.error(f"Error processing visit: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/api/reset", methods=["POST"])
def reset_count():
    """Reset visitor count (for testing purposes)"""
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE visitor_stats SET count = 0 WHERE id = ?', ('visitor_count',))
            conn.commit()
            logger.info("Visitor count reset to 0")
            return jsonify({"message": "Visitor count reset", "visits": 0})
    except sqlite3.Error as e:
        logger.error(f"Error resetting count: {e}")
        return jsonify({"error": "Failed to reset count"}), 500

@app.route("/api/status", methods=["GET"])
def status():
    """Get current status without incrementing count"""
    current_count = get_visitor_count()
    has_cookie = bool(request.cookies.get("visited"))
    return jsonify({
        "visits": current_count,
        "has_cookie": has_cookie,
        "database_path": os.path.abspath(DATABASE_PATH)
    })

# Lambda handler for AWS deployment
lambda_handler = Mangum(app)

if __name__ == "__main__":
    logger.info(f"Starting Flask app with SQLite database at: {os.path.abspath(DATABASE_PATH)}")
    app.run(host="0.0.0.0", port=3000, debug=True)