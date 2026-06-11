from waitress import serve
from app import app

if __name__ == '__main__':
    # Serve the app via waitress on localhost port 8080
    print("Starting Waitress server on http://127.0.0.1:8080...")
    serve(app, host='127.0.0.1', port=8080)
