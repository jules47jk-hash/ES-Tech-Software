"""
Production server startup script.
Use this instead of app.py for production deployment.
Run with: gunicorn -w 4 -b 0.0.0.0:5000 start_production:app
Or: python start_production.py (for testing)
"""
from app import app, init_db
import os

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Get port from environment or default to 5000
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    
    # Run in production mode (no debug)
    app.run(host=host, port=port, debug=False)

